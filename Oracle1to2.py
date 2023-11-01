import streamlit as st
from utils import languages


class Oracle1to2():

    def __init__(self, database_single, database_couples, language=languages.ITALIAN) -> None:

        self.single_db = database_single
        self.couple_db = database_couples
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
                self._search_oracle(c1, c2)

    def _search_oracle(self, code_one: str, code_two: str) -> None:
        query_string = {"Id": int(code_one)}
        res = list(self.single_db.find(query_string))

        if len(res) == 0:
            st.warning(
                "The first code does not exist" if self.language == languages.ENGLISH else
                "Nessun risultato, il primo numero è inesistente")
        else:
            number = res[0]["coppia"]["Id"]
            if int(code_two) == int(number):
                self._successful_match(code_one, code_two)
                st.success("It's a match!")
            else:
                st.error("It's not a match :(")

    def _successful_match(self, code_one: str, code_two: str):

        query_string = {"Id": int(code_one)}
        res = list(self.single_db.find(query_string))
        self.single_db.update_one(res[0], {"$set": {"attivo": False}})

        query_string = {"Id": int(code_two)}
        res2 = list(self.single_db.find(query_string))
        self.single_db.update_one(res2[0], {"$set": {"attivo": False}})

        new_couple = {
            "nomicognomi": [res[0]["nomecognome"], res2[0]["nomecognome"]],
            "ids": [res[0]["Id"], res2[0]["Id"]],
            "attivo": True,
            "squadra": res2[0]["squadra"],
            "nomi": f'{res[0]["nomecognome"]} - {res2[0]["nomecognome"]}',
            "available": True
        }

        self.couple_db.insert_one(new_couple)
