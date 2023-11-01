from databases.couples_database import CouplesDB
from utils import languages
import streamlit as st

class Oracle2to4():

    def __init__(self, database_couples: CouplesDB, database_quartets, database_admin, language=languages.ITALIAN) -> None:

        self.couple_db : CouplesDB = database_couples
        self.quartets_db = database_quartets
        self.admin_db = database_admin
        self.language = language

    def show_page(self) -> None:

        if self.language == languages.ITALIAN:
            self._show_page_italian()
        elif self.language == languages.ENGLISH:
            raise NotImplemented("Only Italian is available")


    def _show_page_italian(self) -> None:
        active_couples = self.couple_db.get_active_couples()

        if len(active_couples) == 0:
            st.write("Nessuna coppia in questa fase")
            return

        with st.form("Ricerca oracolo coppie"):

            first_couple = st.selectbox("Prima coppia", active_couples)
            second_couple = st.selectbox("Seconda coppia", active_couples)

            submitted = st.form_submit_button("Forma")
            if submitted and first_couple != second_couple:
                if self.couple_db.check_quartet(first_couple, second_couple):
                    self.merge_couples(active_couples, first_couple, second_couple)
                else:
                    st.error("Queste due coppie non appartengono alla stessa squadra :(")

    def merge_couples(self, couples, first_couple, second_couple):

        # Handling teams that have size not power of two
        if not self.couple_belongs_to_sextet(first_couple):
            self.create_quartet(first_couple, second_couple)
            st.success("Quartetto formato!\n Avanzate alla prossima fase!")
        else:
            self._handle_sextet(couples, first_couple, second_couple)

    def _handle_sextet(self, active_couples, first_couple, second_couple):
        st.warning(
            "Siete nella stessa squadra ma formerete un sestetto. Aspettate l'ultima coppia della vostra squadra.")
        st.write(
            "Se invece è disponibile una terza coppia potete provare a inserirla per vedere se siete nella stessa squadra")

        third_couple = st.selectbox("Terza coppia", active_couples[::-1])
        if (self.couple_db.check_quartet(first_couple, third_couple)
                and first_couple != third_couple
                and second_couple != third_couple
            ):
            self.create_sextet(first_couple, second_couple, third_couple)
            st.success("Sestetto formato!\n Avanzate alla prossima fase!")
        else:
            st.error(
                "Queste due coppie non appartengono alla stessa squadra o non sono tre coppie diverse:(")
            st.write("Assicurarsi che i tre selectbox contengano tre coppie diverse")

    def create_quartet(self, first_couple, second_couple):

        self.couple_db.mark_inactive(first_couple)
        self.couple_db.mark_inactive(second_couple)

        self.quartets_db.insert_quartet(
            self.couple_db.search(first_couple)[0],
            self.couple_db.search(second_couple)[0]
        )

        team = self.couple_db.search(first_couple)[0]["squadra"]
        self.admin_db.inform_quartet(team)

    def couple_belongs_to_sextet(self, first_couple):

        team = self.couple_db.search_name(first_couple)[0]["nomi"]
        this_team_quartets = self.admin_db.search_team_quartets(team)

        if len(this_team_quartets) == 0:
            return False
        else:
            return this_team_quartets[0]["counter"] == 3

    def create_sextet(self, first_couple, second_couple, third_couple):

        self.couple_db.mark_inactive(first_couple)
        self.couple_db.mark_inactive(second_couple)
        self.couple_db.mark_inactive(third_couple)

        self.quartets_db.insert_sextet(
            self.couple_db.search(first_couple)[0],
            self.couple_db.search(second_couple)[0],
            self.couple_db.search(third_couple)[0]
        )

        team = self.couple_db.search(first_couple)[0]["squadra"]
        self.admin_db.inform_quartet(team)




