from APIs.API import GenreAPI

class RedisGenreAPI(GenreAPI.GenreAPI):

    db = None

    def __init__(self, db):
        self.db = db

    def addGenre(self, type):
        return NotImplementedError("Not implemented")