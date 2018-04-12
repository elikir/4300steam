
class UserAPI(object):




    def addUser(self, userID, password):
        return NotImplementedError("Not implemented")

    def addGame(self, gameID):
        return NotImplementedError("Not implemented")

    def addItem(self, itemID):
        return NotImplementedError("Not implemented")

    def addBalance(self, amount):
        return NotImplementedError("Not implemented")

    def reduceBalance(self, amount):
        return NotImplementedError("Not implemented")

    def addFriend(self, friendID):
        return NotImplementedError("Not implemented")

    def messageFriend(self, friend, message_content):
        return NotImplementedError("Not implemented")

    def validLogon(self, userID, password):
        return NotImplementedError("Not implemented")

    def getBalance(self, userID):
        return NotImplementedError("Not implemented")

    def getLibrary(self, userID):
        return NotImplementedError("Not implemented")

    def getInventory(self, userID):
        return NotImplementedError("Not implemented")

    def getFriendList(self, userID):
        return NotImplementedError("Not implemented")

    def makeBuyOrder(self, userID, itemID, price):
        return NotImplementedError("Not implemented")

    def makeSellOrder(self, userID, itemID, price):
        return NotImplementedError("Not implemented")

    def getTransactions(self, userID):
        return NotImplementedError("Not implemented")
