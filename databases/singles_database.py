from databases.abstract_database import AbstractDatabase


class SinglesDB(AbstractDatabase):

    def __init__(self, database):

        super().__init__(database)

    def stand_status_update(self, my_id, stand):
        """
        Function to store the completion of a stand by a given player
        :param my_id: id of the player that has completed the game
        :param stand: stand letter (A, B...)
        """
        player = list(self.db.find({"Id": my_id}))[0]

        if player["stand_visitati"][stand]:
            return False
        else:
            self.db.update_one(player, {"$set": {"stand_visitati." + stand: True}})
            return True

    def get_all_names(self):
        """
        Function to get the names of all partecipants (used in the search bar)
        :return: dict of tuples key = first last, value = (my_id, other's id)
        """
        partecipants = list(self.db.find({}))
        targets = {}
        for partecipant in partecipants:
            first = partecipant["Nome"]
            last = partecipant["Cognome"]
            if "coppia" in partecipants:
                targets[f"{first} {last}"] = (int(partecipant["Id"]), int(partecipant["coppia"]["Id"]))
        return targets