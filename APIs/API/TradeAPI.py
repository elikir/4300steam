

class TradeAPI(object):

    def createTrade(self, userFrom, userTo, offerItems, forItems):
        return NotImplementedError("Not implemented")

    def acceptTrade(self, tradeID):
        return NotImplementedError("Not implemented")

    def rejectTrade(self, tradeID):
        return NotImplementedError("Not implemented")

    def getTradeInfo(self, tradeID):
        return NotImplementedError("Not implemented")