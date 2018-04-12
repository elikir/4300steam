from APIs.API import ItemAPI

class RedisItemAPI(ItemAPI.ItemAPI):

    db = None

    def __init__(self, db):
        self.db = db

    def addItem(self, itemID, name, gameID, description, imageLink = None):
        keyName = "item:{}:name".format("itemID")
        keyGameID = "item:{}:game".format("itemID")
        keyDesc = "item:{}:desc".format("itemID")
        self.db.set(keyName, name)
        self.db.set(keyGameID, gameID)
        self.db.set(keyDesc, description)


    def addOrder(self, type, itemID, orderID):
        key = "item:{}:{}".format(itemID, type)
        self.db.lpush(key, orderID)


    def getItemInfo(self, itemID):
        keyName = "item:{}:name".format("itemID")
        keyGameID = "item:{}:game".format("itemID")
        keyDesc = "item:{}:desc".format("itemID")

        return {
            "name": self.db.get(keyName),
            "gameName": self.db.get("game:{}:title".format(self.db.get(keyGameID))),
            "description": self.db.get(keyDesc)
        }