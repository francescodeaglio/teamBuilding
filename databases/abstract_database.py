class AbstractDatabase():

    def __init__(self, database):
        self.db = database

    def mark_inactive(self, code: int) -> None:
        query_string = {"Id": code}
        res = list(self.db.find(query_string))
        self.db.update_one(res[0], {"$set": {"attivo": False}})

    def search(self, code: int) -> list:
        query_string = {"Id": code}
        return list(self.db.find(query_string))