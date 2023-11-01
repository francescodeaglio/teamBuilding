

class AdminDB():

    def __init__(self, db):
        self.db = db


    def inform_quartet(self, team: str) -> None:

        this_team_quartets = list(self.db.find({
            "fase": "quartetti",
            "squadra": team
        }))

        if len(this_team_quartets) == 0:
            self.db.insert_one(
                {
                    "fase": "quartetti",
                    "squadra": team,
                    "counter": 1
                }
            )
        else:
            self.db.update_one(this_team_quartets[0], {"$set": {
                "counter": int(this_team_quartets[0]["counter"]) + 1
            }})

    def search_team_quartets(self, team):
        return list(self.db.find({
            "fase": "quartetti",
            "squadra": team
        }))