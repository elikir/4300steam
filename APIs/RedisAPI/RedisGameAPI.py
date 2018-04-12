from APIs.API import GameAPI

class RedisGameAPI(GameAPI.GameAPI):
    db = None

    def __init__(self, db):
        self.db = db

    def addGame(self, gameID, gameName, genre, price, description, achievements):

        self.db.set("game:{}:title".format(gameID), gameName)
        self.db.set("game:{}:genre".format(gameID), genre)
        self.db.set("game:{}:description".format(gameID), description)
        self.db.set("game:{}:price".format(gameID), price)
        self.db.sadd("game:{}:achievements".format(gameID), achievements)


    def getPrice(self, gameID):
        return float(self.db.get("game:{}:price".format(gameID)))


    def getGameInfo(self, gameID):
        return {
            "title":self.db.get("game:{}:title".format(gameID)),
            "genre":self.db.get("game:{}:genre".format(gameID)),
            "description":self.db.get("game:{}:description".format(gameID))}
