from databases.abstract_database import AbstractDatabase


class SinglesDB(AbstractDatabase):

    def __init__(self, database):

        super().__init__(database)

    def stand_status_update(self, my_id, stand):
        """
        Function to store the completion of a stand by a given player
        :param my_id: id of the player that has completed the game
        :param others_id: id of the other player in the couple
        :param stand: stand letter (A, B...)
        """
        player = list(self.db.find({"Id": my_id}))[0]

        if player["stand_visitati"][stand]:
            return False
        else:
            self.db.update_one(player, {"$set": {"stand_visitati." + stand: True}})
            return True
