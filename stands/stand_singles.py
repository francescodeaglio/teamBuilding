import streamlit as st

from utils import get_stands_description_singles


class StandSingles:

    def __init__(self, stand, singles_db):
        self.stand = stand
        self.stand_letter = stand.split("-")[0].strip()
        self.singles_db = singles_db
        self.stand_description = get_stands_description_singles()[self.stand_letter]

    def show_page(self):
        st.markdown(f"###### Descrizione stand\n\n {self.stand_description}")

        with st.form("Ricerca stand"):

            if "cached_ids" not in st.session_state:
                partecipants = self.singles_db.get_all_names()
                st.session_state["cached_ids"] = partecipants
            else:
                partecipants = st.session_state["cached_ids"]

            partecipant = st.selectbox("Cerca il partecipante", partecipants)
            my_id, other_id = partecipants[partecipant]

            submitted = st.form_submit_button("Cerca")
            if submitted:
                success = self.singles_db.update_stand_status(my_id, self.stand_letter)
                if success:
                    st.success("Consegna la busta numero " + str(other_id))
                else:
                    st.error(f"Il giocatore {my_id} ha già visitato questo stand!")
