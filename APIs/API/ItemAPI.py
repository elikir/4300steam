

class ItemAPI(object):

    def addItem(self, name, gameId, description, imageLink):
        return NotImplementedError("Not implemented")

    def addBuyOrder(self, buyerID, wantingPrice):
        return NotImplementedError("Not implemented")

    def addSellOrder(self, sellerID, askingPrice):
        return NotImplementedError("Not implemented")
