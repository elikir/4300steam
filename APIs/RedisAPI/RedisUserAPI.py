from APIs.API import UserAPI

class RedisUserAPI(UserAPI.UserAPI):

    db = None
    messenger = None
    market = None
    order = None
    items = None
    games = None
    trades = None
    market = None

    def __init__(self, db, messenger, orders, items, games, trades, market):
        self.db = db
        self.messenger = messenger
        self.orders = orders
        self.items = items
        self.games = games
        self.trades = trades
        self.market = market


    def addUser(self, userID, password):
        self.db.set(userID, password)
        self.db.set("user:{}:balance".format(userID), 0)

    def addGame(self,userID, gameID):
        key = "user:{}:library".format(userID)
        self.db.sadd(key, gameID)

    def buyGame(self, userID, gameID):
        gamePrice = self.games.getPrice(gameID)

        if gamePrice <= self.getBalance(userID):
            self.addGame(userID, gameID)
            self.reduceBalance(userID, gamePrice)
            return True

        return False


    def addItem(self,userID, itemID):
        key = "user:{}:inventory".format(userID)
        self.db.sadd(key, itemID)

    def moveItem(self, fromID, toID, itemID):
        key1 = "user:{}:inventory".format(fromID)
        self.db.srem(key1, [itemID])
        self.addItem(toID, itemID)

    def addBalance(self,userID, amount):
        key = "user:{}:balance".format(userID)
        self.db.set(key, self.getBalance(userID) + amount)

    def reduceBalance(self,userID, amount):
        key = "user:{}:balance".format(userID)
        self.db.set(key, self.getBalance(userID) - amount)

    def addFriend(self,userID, friendID):
        if self.db.exists(friendID):
            key1 = "user:{}:friendList".format(userID)
            key2 = "user:{}:friendList".format(friendID)
            self.db.sadd(key1, friendID)
            self.db.sadd(key2, userID)

    def messageFriend(self,userID, friend, message_content):
        msg_uuid = self.messenger.sendMessage(userID, friend, message_content)
        key1 = "user:{}:friend:{}:messages".format(userID, friend)
        key2 = "user:{}:friend:{}:messages".format(friend, userID)

        self.db.lpush(key1, msg_uuid)
        self.db.lpush(key2, msg_uuid)

    def validLogon(self, userID, password):
        return self.db.get(userID) == password


    def getBalance(self, userID):
        key = "user:{}:balance".format(userID)
        return float(self.db.get(key))

    def getLibrary(self, userID):
        key = "user:{}:library".format(userID)
        return [ self.games.getGameInfo(x) for x in self.db.smembers(key)]

    def getInventory(self, userID):
        key = "user:{}:inventory".format(userID)
        inventory =  self.db.smembers(key)
        inv = []
        for item in inventory:
            inv.append(self.items.getItemInfo(item))
        return inv

    def getFriendList(self, userID):
        key = "user:{}:friendList".format(userID)
        return self.db.smembers(key)

    def getMessages(self, userID, friendID):
        key = "user:{}:friend:{}:messages".format(userID, friendID)
        return [{"message" : self.messenger.getMessageContents(x),
                "from" : self.messenger.getMessageFrom(x),
                "to" : self.messenger.getMessageTo(x)}
                for x in self.db.lmembers(key)]

    def makeOrder(self, type, userID, itemID, price):
        self.db.ladd("user:{}:{}".format(userID, type),
            self.orders.makeOrder(type, userID, itemID, price))

    def makeTradeOffer(self, userFrom, userTo, offerItems, forItems):
        tradeID = self.trades.createTrade(userFrom, userTo, offerItems, forItems)
        self.db.lpush("user:{}:trades:outgoing".format(userFrom),tradeID)
        self.db.lpush("user:{}:trades:incoming".format(userTo), tradeID)
        return tradeID

    def getTradeOffers(self, userID, type):
        return self.db.lmembers("user:{}:trades:{}".format(userID, type))


    def acceptTrade(self, tradeID):
        print self.trades.getTradeInfo(tradeID)
        if int(self.db.get("trade:{}:completed".format(tradeID))) == 0:
            key1 = "trade:{}:userFrom".format(tradeID)
            key2 = "trade:{}:userTo".format(tradeID)
            key3 = "trade:{}:offerItems".format(tradeID)
            key4 = "trade:{}:forItems".format(tradeID)


            for offerItem in self.db.lmembers(key3):
                print offerItem
                self.moveItem(self.db.get(key1), self.db.get(key2), offerItem)

            for forItem in self.db.lmembers(key4):
                self.moveItem(self.db.get(key2), self.db.get(key1), forItem)

            self.db.set("trade:{}:completed".format(tradeID), True)

    def rejectTrade(self, tradeID):
        if int(self.db.get("trade:{}:completed".format(tradeID))) == 0:
            key1 = "trade:{}:userFrom".format(tradeID)
            key2 = "trade:{}:userTo".format(tradeID)
            key3 = "trade:{}:offerItems".format(tradeID)
            key4 = "trade:{}:forItems".format(tradeID)
            self.db.delete(key1)
            self.db.delete(key2)
            self.db.delete(key3)
            self.db.delete(key4)