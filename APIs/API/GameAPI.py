

class GameAPI(object):

    def addGame(self, gameID, gameName, genreID, price, description, achievements):
        return NotImplementedError("Not implemented")

    def getPrice(self, gameID):
        return NotImplementedError("Not implemented")