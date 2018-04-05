

class GameAPI(object):

    def addGame(self, gameName, genreID, price, description, achievements):
        return NotImplementedError("Not implemented")

    def getPrice(self):
        return NotImplementedError("Not implemented")