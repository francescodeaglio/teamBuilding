from databases import SinglesDB, CouplesDB, QuartetsDB, OctectsDB
import streamlit as st


class ActivePlayersMessage:

    def __init__(self, singles_db: SinglesDB, couples_db: CouplesDB, quartets_db: QuartetsDB, octets_db: OctectsDB):
        self.singles_db = singles_db
        self.couples_db = couples_db
        self.quartets_db = quartets_db
        self.octects_db = octets_db

    def show_awaiting(self):
        st.code(
            "Awaiting = persone che han completato uno stand e stanno aspettando l'altra coppia della propria squadra")
        awaiting = list(self.couples_db.find({"awaiting": True, "attivo": True}))
        st.write(
            "\n".join([f'Squadra {int(x["squadra"])} : {x["nomi"]}' for x in awaiting])
        )

    def show_active_third(self):
        active_players = self.quartets_db.find_all()
        elenco = {squadra: [] for squadra in "12345"}

        for player in active_players:
            s = f'Quartetto **{player["nomi"]}**'
            if "altri" not in player:
                s += " non è ancora stato definito l'altro quartetto"
            else:
                if player["altri"]["tipo"] == "quartetto":
                    s += f' stanno cercando **{player["altri"]["nomi_quartetto"]}**'
                else:
                    s += f' per ora stanno cercando **{player["altri"]["nomi_coppia"]}**'
            elenco[str(int(player["squadra"]))].append(s)

        for team in sorted(list(elenco.keys())):
            st.write("#### Squadra: " + team)
            if len(elenco[team]) == 0:
                st.write("Nessun quartetto attivo")
            else:
                st.markdown("\n\n".join(elenco[team]))

    def show_active_fourth(self):
        active_players = self.octects_db.find_all()
        elenco = {squadra: [] for squadra in "12345"}
        for player in active_players:
            s = f'Ottetto **{player["nomi"]}**'
            elenco[str(int(player["squadra"]))].append(s)

        for team in sorted(list(elenco.keys())):
            st.write("#### Squadra: " + team)
            if len(elenco[team]) == 0:
                st.write("Nessun ottetto completato")
            else:
                st.markdown("\n".join(elenco[team]))
