import certifi
import pymongo

import pymongo
import certifi
from databases import AdminDB, SinglesDB, CouplesDB, OctectsDB, QuartetsDB


class MongoHandler():

    def __init__(self):
        ca = certifi.where()
        client = pymongo.MongoClient(
            "mongodb+srv://campoestivo:qVx8khSNIljjfKqw@cluster0.usbb0.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=ca
        )
        db = client.testOpening
        self.singles_db = SinglesDB(db["iscritti"])
        self.couples_db = CouplesDB(db["coppie"])
        self.quartets_db = QuartetsDB(db["quartetti"])
        self.octets_db = OctectsDB(db["otteti"])
        self.admin_db = AdminDB(db["gestionale"])
