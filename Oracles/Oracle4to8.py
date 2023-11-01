from Databases.OctetsDB import OctectsDB
from Databases.QuartetsDB import QuartetsDB
from utils import languages
import streamlit as st

class Oracle4to8():

    def __init__(self, database_quartets: QuartetsDB, database_octets: OctectsDB,
                 language=languages.ITALIAN) -> None:

        self.quartets_db: QuartetsDB = database_quartets
        self.octects_db : OctectsDB = database_octets
        self.language = language

    def show_page(self) -> None:

        if self.language == languages.ITALIAN:
            self._show_page_italian()
        elif self.language == languages.ENGLISH:
            raise NotImplemented("Only Italian is available")

    def _show_page_italian(self):
        with st.form("Ricerca oracolo - Ottetti"):
            st.write("Inserisci il codice di un membro di ognuno dei due quartetti")
            first_quartet = st.text_input('Inserisci il codice di un membro del primo quartetto')
            second_quartet = st.text_input('Inserisci il codice di un membro del secondo quartetto')

            submitted = st.form_submit_button("Cerca")
            if submitted:
                self.search_octect(first_quartet, second_quartet)

    def search_octect(self, first_quartet, second_quartet):

        all_quartets = self.quartets_db.find_all()

        for quartet in all_quartets:

            if self._suitable_octect(first_quartet, second_quartet, quartet):
                self.create_octet(first_quartet, second_quartet)
                st.success("It's a match!")
                return

        st.error("Non siete insieme :(\t Continuate a cercare!")

    def _suitable_octect(self, first_quartet, second_quartet, iter_quartet):

        iter_quartet_is_first = int(first_quartet) in [int(id) for id in iter_quartet["ids"]]
        iter_quartet_is_second = int(second_quartet) in [int(id) for id in iter_quartet["ids"]]

        other_quartet_is_first = int(first_quartet) in [int(id) for id in iter_quartet["altri"]["ids"]]
        other_quartet_is_second = int(second_quartet) in [int(id) for id in iter_quartet["altri"]["ids"]]

        return ((iter_quartet_is_first and other_quartet_is_second) or
                (iter_quartet_is_second and other_quartet_is_first))

    def create_octet(self, first_quartet, second_quartet):

        first_doc = self.quartets_db.mark_inactive_from_single_id(first_quartet)
        second_doc = self.quartets_db.mark_inactive_from_single_id(second_quartet)

        self.octects_db.insert_octet(
            first_doc,
            second_doc
        )
