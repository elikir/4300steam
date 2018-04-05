from APIs.API import GameAPI

class RedisGameAPI(GameAPI.GameAPI):
    db = None

    def __init__(self, db):
        self.db = db

    def addGame(self, gameName, genreID, price, description, achievements):
        return NotImplementedError("Not implemented")
