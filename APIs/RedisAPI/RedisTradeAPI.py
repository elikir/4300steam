from APIs.API import TradeAPI

import string
import random

class RedisTradeAPI(TradeAPI.TradeAPI):

    db = None
    users = None

    def __init__(self, db):
        self.db = db




    def createTrade(self, userFrom, userTo, offerItems, forItems):
        uuid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

        key1 = "trade:{}:userFrom".format(uuid)
        key2 = "trade:{}:userTo".format(uuid)
        key3 = "trade:{}:offerItems".format(uuid)
        key4 = "trade:{}:forItems".format(uuid)
        self.db.set("trade:{}:completed".format(uuid), 0)

        self.db.set(key1, userFrom)
        self.db.set(key2, userTo)
        self.db.ladd(key3, offerItems)
        self.db.ladd(key4, forItems)

        return uuid





    def getTradeInfo(self, tradeID):
        return {
            "from": self.db.get("trade:{}:userFrom".format(tradeID)),
        "to": self.db.get("trade:{}:userTo".format(tradeID)),
        "forItems": self.db.lmembers("trade:{}:forItems".format(tradeID)),
        "offerItems": self.db.lmembers("trade:{}:offerItems".format(tradeID)),
            "completed": self.db.get("trade:{}:completed".format(tradeID))
        }

