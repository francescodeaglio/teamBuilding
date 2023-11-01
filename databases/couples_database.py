from databases.abstract_database import AbstractDatabase


class CouplesDB(AbstractDatabase):

    def __init__(self, database):

        super().__init__(database)

    def insert_couple(self, first_component, second_component) -> None:

        new_couple = {
            "nomicognomi": [first_component["nomecognome"], second_component["nomecognome"]],
            "ids": [first_component["Id"], second_component["Id"]],
            "attivo": True,
            "squadra": first_component["squadra"],
            "nomi": f'{first_component["nomecognome"]} - {second_component["nomecognome"]}',
            "available": True
        }

        self.db.insert_one(new_couple)

    def get_active_couples(self) -> list:
        res = self.db.find({})
        return [el["nomi"] for el in res if el["attivo"] == True]

    def check_quartet(self, first_couple, second_couple) -> bool:

        try:
            query_string = {"nomi": first_couple}
            c1 = list(self.db.find(query_string))[0]
            self.db.update_one(c1, {"$set": {"awaiting": True}})

            query_string = {"nomi": second_couple}
            c2 = list(self.db.find(query_string))[0]
            self.db.update_one(c2, {"$set": {"awaiting": True}})

            return c1["squadra"] == c2["squadra"]
        except:
            return False

    def search_name(self, name):
        query_string = {"nomi": name}
        return  list(self.db.find(query_string))

    def get_awaiting_suitable_couples(self, team):
        return list(
            self.db.find({"squadra":team, "awaiting": True, "attivo": True, "available": True}))

    def register_precoupling(self, couple):
        self.db.update_one(
            couple,
            {"$set": {"available": False}}
        )

    def players_active(self, names):
        r = self.db.find({"nomi": names})[0]

        return r["attivo"]

    def search_couple_names(self, names):
        return self.db.find({"nomi": names})[0]
