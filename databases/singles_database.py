from databases.abstract_database import AbstractDatabase


class SinglesDB(AbstractDatabase):

    def __init__(self, database):

        super().__init__(database)