from databases import SinglesDB, CouplesDB, QuartetsDB
from utils import get_descrizione_quartetti
import streamlit as st

class StandQuartets:

    def __init__(self, stand: str, singles_db: SinglesDB, couples_db: CouplesDB, quartets_db: QuartetsDB ):
        self.singles_db = singles_db
        self.couples_db = couples_db
        self.quartets_db = quartets_db

        self.stand = stand
        self.stand_letter = stand.split("-")[0].strip()
        self.stand_description = get_descrizione_quartetti()[self.stand_letter]


    def show_page(self):
        st.markdown(f"###### Descrizione stand\n\n {self.stand_description}")

        with st.form("Ricerca stand - quartetti"):
            quartets = self.quartets_db.find_all_names()

            names = st.selectbox("Cerca il quartetto", quartets)
            submitted = st.form_submit_button("Cerca")
            if submitted:
                self.stand_status_update(names)

    def stand_status_update(self, names):
            players = self.quartets_db.find_names(names)[0]

            # check if this players have already another matched quartet
            if "altri" in players:
                return self._handle_quartet_with_existing_peer(players)
            else:
                return self._handle_quartet_without_existing_peer(players, names)

    def _handle_quartet_without_existing_peer(self, players, names):
        # altrimenti dobbiamo assegnarlo
        eligible_quartets = self.quartets_db.get_suitable_quartets(players["squadra"], names)

        if len(eligible_quartets) == 0:
            # no other quartets of this team are in phase 3, check if there is a couple waiting at the oracle
            eligible_couples = self.couples_db.get_awaiting_suitable_couples(players["squadra"], )

            if len(eligible_couples) == 0:
                # no couples in phase 2, not handled
                st.success("Andate all'oracolo, dite la parola magica 'epecchè' e ci sarà una sorpresa per voi")
                return
            else:
                # precoupling
                others = eligible_couples[0]
                others_peer = {
                    "tipo": "coppia",
                    "nomi_coppia": others["nomi"],
                    "ids": others["ids"]
                }
                self.quartets_db.register_peer(players, others_peer)
                self.couples_db.register_precoupling(others)

                peer_ids = others["ids"]
        else:
            # create the quartet
            others = eligible_quartets[0]
            self._peer_quartets(players, others)

            peer_ids = others["ids"]

        letter = self.find_suitable(peer_ids)
        self.message(letter)

    def _peer_quartets(self, players, others):
        others_peer = {
            "tipo": "quartetto",
            "nomi_coppia": others["nomi"],
            "ids": others["ids"]
        }
        players_peer = {
            "tipo": "quartetto",
            "nomi_coppia": players["nomi"],
            "ids": players["ids"]
        }
        self.quartets_db.register_peer(players, others_peer)
        self.quartets_db.register_peer(others, players_peer)

    def _handle_quartet_with_existing_peer(self, players):

        if players["altri"]["tipo"] == "coppia":
            # check if the couple evolved to a quartet

            if not self.couples_db.players_active(players["altri"]["nomi_coppia"]):
                # find the quartet
                target_quartet = None
                for quartet in self.quartets_db.find_all():
                    if players["altri"]["nomi_coppia"] in quartet["nomi"]:
                        target_quartet = quartet
                        break

                # update the link
                self._peer_quartets(players, target_quartet)
                peer_ids = target_quartet["ids"]
            else:
                peer_ids = self.couples_db.search_couple_names(players["altri"]["nomi_coppia"])["ids"]
        else:
            peer_ids = players["altri"]["ids"]
        letter = self.find_suitable(peer_ids)
        self.message(letter)

    def message(self, letter):
        if letter is not None:
            st.success(f"Consegna la busta numero {letter}")
        else:
            st.error("Non rimane nessuna busta dell'altro quartetto in questo stand")

    def find_suitable(self, peer_ids):
        for id in peer_ids:
            partecipant = self.singles_db.search(int(id))[0]
            if not partecipant["stand_visitati"][self.stand_letter]:
                self.singles_db.stand_status_update(partecipant,  self.stand_letter)
                return id
        return None

