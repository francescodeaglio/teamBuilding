from Databases.AbstractDatabase import AbstractDatabase


class SinglesDB(AbstractDatabase):

    def __init__(self, database):

        super().__init__(database)