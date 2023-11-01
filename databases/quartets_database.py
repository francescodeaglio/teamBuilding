from databases.abstract_database import AbstractDatabase


class QuartetsDB(AbstractDatabase):

    def __init__(self, database):
        super().__init__(database)


    def insert_quartet(self, first_couple, second_couple):
        quartet = {
            "membri": first_couple["nomicognomi"] + second_couple["nomicognomi"],
            "ids": first_couple["ids"] + second_couple["ids"],
            "attivo": True,
            "squadra": first_couple["squadra"],
            "nomi": f'{first_couple["nomi"]} - {second_couple["nomi"]}',
            "available": True
        }

        if check_precoupling([first_couple, second_couple]):
            others = self._keep_precoupling([first_couple, second_couple])
            quartet["altri"] = others
            quartet["available"] = False

        self.db.insert_one(quartet)

    def insert_sextet(self, first_couple, second_couple, third_couple):
        quartet = {
            "membri": first_couple["nomicognomi"] + second_couple["nomicognomi"] + third_couple["nomicognomi"],
            "ids": first_couple["ids"] + second_couple["ids"] + third_couple["ids"],
            "attivo": True,
            "squadra": first_couple["squadra"],
            "nomi": f'{first_couple["nomi"]} - {second_couple["nomi"]} - {third_couple["nomi"]}',
            "available": True
        }

        if check_precoupling([first_couple, second_couple, third_couple]):
            altri = self._keep_precoupling([first_couple, second_couple, third_couple])
            quartet["altri"] = altri
            quartet["available"] = False

        self.db.insert_one(quartet)

    def _keep_precoupling(self, members):
        assert check_precoupling(members)

        for member in members:
            if member["available"] == False:
                names = member["nomi"]
                break

        for quartetto in self.db.find({}):
            if "altri" in quartetto and quartetto["altri"]["nomi_coppia"] == names:
                return {
                    "tipo": "quartetto",
                    "nomi_quartetto": quartetto["nomi"],
                    "ids": quartetto["ids"]
                }

    def find_all(self) -> list:
        return list(self.db.find({}))

    def find_all_names(self) -> list:
        quartets = list(self.db.find({}))
        names = []
        for quartet in quartets:
            names.append(quartet["nomi"])
        return names

    def mark_inactive_from_single_id(self, id):
        all_quartets = self.db.find({})
        match = None

        for quartet in all_quartets:
            if int(id) in [int(x) for x in quartet["ids"]]:
                match = quartet
                break

        self.db.update_one(match, {"$set": {"attivo": False}})

        return  match

    def get_suitable_quartets(self, team, names):
        return list(
            self.db.find({"squadra": team, "available": True, "nomi": {"$ne": names}})
        )

    def register_peer(self, players, others):
        self.db.update_one(
            players,
            {"$set": {"altri": others}}
        )
        self.db.update_one(
            players,
            {"$set": {"available": False}}
        )

    def find_names(self, names):
        return self.db.find({"nomi":names})


def check_precoupling(members):
    for member in members:
        if member["available"] == False:
            return True
    return False


