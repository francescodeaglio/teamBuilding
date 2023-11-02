from databases import SinglesDB, CouplesDB, QuartetsDB, OctectsDB
import streamlit as st


class PlayerSearch:

    def __init__(self, singles_db: SinglesDB, couples_db: CouplesDB, quartets_db: QuartetsDB, octets_db: OctectsDB):
        self.singles_db = singles_db
        self.couples_db = couples_db
        self.quartets_db = quartets_db
        self.octects_db = octets_db

    def show(self):
        all_names = self.singles_db.get_all_names().keys()
        name = st.selectbox("Seleziona il nome", all_names)

        info = self.singles_db.find_one({"nomecognome": name})
        title = f'#### {name} (Team : {int(info["squadra"])}, Id : {int(info["Id"])})'
        st.write(title)

        strings = []

        # first stage
        string = f'**Fase 1**: {name} {"è attivo" if info["attivo"] == True else "non è attivo"}\n\n'
        stands = [x for x in info["stand_visitati"] if info["stand_visitati"][x] == True]
        string += (f'Ha completato {"gli stand " + "-".join(stands) if len(stands) > 0 else "nessuno stand"} '
                   f'e deve cercare {info["coppia"]["nomecognome"]} (id = {int(info["coppia"]["Id"])})')
        strings.append(string)

        # second stage
        info = self.couples_db.find_one({"nomicognomi": name})

        if info is None:
            string = f'**Fase 2**: {name} non è attivo'
        else:
            string = f'**Fase 2**: {name} {"è attivo" if info["attivo"] == True else "non è attivo"}'
            if info["awaiting"] == True and info["attivo"] == True:
                string += "\n\nAl momento sta aspettando una coppia disponibile della sua squadra"
        strings.append(string)

        # third stage
        info = self.quartets_db.find_one({"membri": name})
        if info is None:
            string = f'**Fase 3**: {name} non è attivo'
        else:
            string = f'**Fase 3**: {name} {"è attivo" if info["attivo"] == True else "non è attivo"}\n\n'
            string += f'Fa parte del quartetto *{info["nomi"]}* i cui id sono rispettivamente {info["ids"]}\n\n'
            if "altri" not in info:
                string += "Non è ancora stato definito l'altro quartetto"
            else:
                if info["altri"]["tipo"] == "quartetto":
                    string += f'Stanno cercando *{info["altri"]["nomi_quartetto"]}* i cui id sono rispettivamente {info["altri"]["ids"]}'
                else:
                    string += f' per ora stanno cercando *{info["altri"]["nomi_coppia"]}* i cui id sono rispettivamente {info["altri"]["ids"]}'
        strings.append(string)

        # last stage
        info = self.octects_db.find_one({"nomicognomi": name})
        if info is None:
            string = f'**Fase 4**: {name} non è attivo'
        else:
            string = f'**Fase 4**: {name} {"è attivo" if info["attivo"] == True else "non è attivo"}\n\n'
            string += f'Fa parte dell ottetto *{info["nomi"]}*'
        strings.append(string)

        out = "\n\n".join(strings)
        st.markdown(out)