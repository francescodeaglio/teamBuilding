import streamlit as st

from databases import SinglesDB, CouplesDB
from utils import languages


class Oracle1to2():

    def __init__(self, database_single: SinglesDB, database_couples: CouplesDB, language=languages.ITALIAN) -> None:

        self.single_db : SinglesDB= database_single
        self.couple_db : CouplesDB = database_couples
        self.language = language

    def show_page(self) -> None:

        if self.language == languages.ITALIAN:
            self._show_page_italian()
        elif self.language == languages.ENGLISH:
            self._show_page_english()

    def _show_page_italian(self) -> None:
        with st.form("Ricerca oracolo"):
            st.write("Inserisci i due codici cercati")
            c1 = st.text_input('Inserisci il primo codice')
            c2 = st.text_input('Inserisci secondo codice')

            submitted = st.form_submit_button("Cerca")
            if submitted:
                self._search_oracle(c1, c2)

    def _show_page_english(self) -> None:
        with st.form("Oracle search"):
            st.write("Please insert the two codes")
            c1 = st.text_input('Insert the first code')
            c2 = st.text_input('Insert the second code')

            submitted = st.form_submit_button("Search")
            if submitted:
                self._search_oracle(int(c1), int(c2))

    def _search_oracle(self, code_one: int, code_two: int) -> None:

        res = self.single_db.search(code_one)

        if len(res) == 0:
            st.warning(
                "The first code does not exist" if self.language == languages.ENGLISH else
                "Nessun risultato, il primo numero è inesistente")
        else:
            matching_number = res[0]["coppia"]["Id"]
            if code_two == matching_number:
                self._successful_match(code_one, code_two)
                st.success("It's a match!")
            else:
                st.error("It's not a match :(")

    def _successful_match(self, code_one: int, code_two: int):

        self.single_db.mark_inactive(code_one)
        self.single_db.mark_inactive(code_two)

        self.couple_db.insert_couple(
            self.single_db.search(code_one)[0],
            self.single_db.search(code_two)[0],
        )


