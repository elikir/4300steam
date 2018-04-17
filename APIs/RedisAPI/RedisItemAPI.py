from APIs.API import ItemAPI


class RedisItemAPI(ItemAPI.ItemAPI):
    db = None
    orders = None
    market = None

    def __init__(self, db, orders, market):
        self.db = db
        self.orders = orders
        self.market = market

    def addItem(self, itemID, name, gameID, description, imageLink=None):
        keyName = "item:{}:name".format(itemID)
        keyGameID = "item:{}:game".format(itemID)
        keyDesc = "item:{}:desc".format(itemID)
        self.db.set(keyName, name)
        self.db.set(keyGameID, gameID)
        self.db.set(keyDesc, description)

    def addOrder(self, type, itemID, orderID):
        key = "item:{}:{}".format(itemID, type)
        self.db.rpush(key, orderID)

    def getItemInfo(self, itemID):
        keyName = "item:{}:name".format(itemID)
        keyGameID = "item:{}:game".format(itemID)
        keyDesc = "item:{}:desc".format(itemID)

        return {
            "name": self.db.get(keyName),
            "gameName": self.db.get("game:{}:title".format(self.db.get(keyGameID))),
            "description": self.db.get(keyDesc)
        }

    def getOrders(self, itemID, type):
        key = "item:{}:{}".format(itemID, type)
        return [self.orders.getOrderInfo(x) for x in self.db.lmembers(key)]

    def addTransaction(self, itemID, price):
        transactionID = self.market.addTransaction(itemID, price)
        key = "item:{}:transactions".format(itemID)
        self.db.lpush(key, transactionID)

    def getPastTransactions(self, itemID):
        key = "item:{}:transactions".format(itemID)
        return [self.market.getTransactionInfo(x) for x in self.db.lmembers(key)]
