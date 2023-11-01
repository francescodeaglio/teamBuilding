from databases.abstract_database import AbstractDatabase


class OctectsDB(AbstractDatabase):

    def __init__(self, database):
        super().__init__(database)

    def insert_octet(self, first_doc, second_doc):
        ottetto = {

            "membri": first_doc["membri"] + second_doc["membri"],
            "ids": first_doc["ids"] + second_doc["ids"],
            "attivo": True,
            "squadra": first_doc["squadra"],
            "nomi": f'{first_doc["nomi"]} - {second_doc["nomi"]}',
            "available": True
        }

        self.db.insert_one(ottetto)
