from APIs.API import UserAPI


class RedisUserAPI(UserAPI.UserAPI):
    db = None
    messenger = None
    market = None
    order = None
    items = None
    games = None
    trades = None

    def __init__(self, db, messenger, orders, items, games, trades):
        self.db = db
        self.messenger = messenger
        self.orders = orders
        self.items = items
        self.games = games
        self.trades = trades

    def addUser(self, userID, password):
        if self.db.inSet("steam:users", userID):
            return False
        self.db.set(userID, password)
        self.db.set("user:{}:balance".format(userID), 0)
        self.db.sadd("steam:users", userID)
        return True

    def addGame(self, userID, gameID):
        key = "user:{}:library".format(userID)
        self.db.sadd(key, gameID)

    def buyGame(self, userID, gameID):
        gamePrice = self.games.getPrice(gameID)

        if gamePrice <= self.getBalance(userID):
            self.addGame(userID, gameID)
            self.reduceBalance(userID, gamePrice)
            return True

        return False

    def addItem(self, userID, itemID):
        key = "user:{}:inventory".format(userID)
        self.db.lpush(key, itemID)

    def moveItem(self, fromID, toID, itemID):
        print toID, fromID, itemID
        key1 = "user:{}:inventory".format(fromID)
        self.db.lrem(key1, [itemID])
        self.addItem(toID, itemID)

    def addBalance(self, userID, amount):
        key = "user:{}:balance".format(userID)
        self.db.set(key, self.getBalance(userID) + amount)

    def reduceBalance(self, userID, amount):
        key = "user:{}:balance".format(userID)
        self.db.set(key, self.getBalance(userID) - amount)

    def addFriend(self, userID, friendID):
        if self.db.exists(friendID):
            key1 = "user:{}:friendList".format(userID)
            key2 = "user:{}:friendList".format(friendID)
            self.db.sadd(key1, friendID)
            self.db.sadd(key2, userID)

    def messageFriend(self, userID, friend, message_content):
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
        return [self.games.getGameInfo(x) for x in self.db.smembers(key)]

    def getInventory(self, userID):
        key = "user:{}:inventory".format(userID)
        return [self.items.getItemInfo(item) for item in self.db.lmembers(key)]

    def getFriendList(self, userID):
        key = "user:{}:friendList".format(userID)
        return self.db.smembers(key)

    def getMessages(self, userID, friendID):
        key = "user:{}:friend:{}:messages".format(userID, friendID)
        return [{"message": self.messenger.getMessageContents(x),
                 "from": self.messenger.getMessageFrom(x),
                 "to": self.messenger.getMessageTo(x)}
                for x in self.db.lmembers(key)]

    def makeOrder(self, type, userID, itemID, price, orderID):
        print orderID
        self.db.lpush("user:{}:order:{}".format(userID, type),
                     orderID)

    def makeTradeOffer(self, userFrom, userTo, offerItems, forItems):
        tradeID = self.trades.createTrade(userFrom, userTo, offerItems, forItems)
        self.db.lpush("user:{}:trades:outgoing".format(userFrom), tradeID)
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

    def getOrders(self, userID, type):
        key = "user:{}:order:{}".format(userID, type)
        return self.db.lmembers(key)

    def makeBuyOrder(self, userID, itemID, price):
        if price > self.getBalance(userID):
            return

        currentSellOrders = self.items.getOrders(itemID, "sell")
        print currentSellOrders
        sold = False

        for order in currentSellOrders:
            if order["price"] <= price:
                self.db.lrem("item:{}:sell".format(itemID), order["id"])
                self.moveItem("ADMIN", userID, order["itemID"])
                self.addBalance(order["userID"], order["price"])
                self.reduceBalance(userID, order["price"])
                sold = True
                break

        if not sold:
            self.reduceBalance(userID, price)
            orderID = self.orders.makeOrder("buy", userID, itemID, price)
            self.makeOrder("buy", userID, itemID, price, orderID)
            self.items.addOrder("buy",
                                itemID,self.orders.makeOrder("buy", userID, itemID, price))

    def makeSellOrder(self, userID, itemID, price):
        currentBuyOrders = self.items.getOrders(itemID, "buy")
        bought = False

        for order in currentBuyOrders:
            if order["price"] >= price:
                self.db.lrem("item:{}:buy".format(itemID), order["id"])
                self.moveItem(userID, order["userID"], order["itemID"])
                self.addBalance(userID, price)
                self.addBalance(order["userID"], order["price"] - price)
                bought = True
                break

        if not bought:
            self.moveItem(userID, "ADMIN", itemID)
            orderID = self.orders.makeOrder("sell", userID, itemID, price)
            self.makeOrder("sell", userID, itemID, price, orderID)
            self.items.addOrder("sell", itemID, orderID)

    def cancelOrder(self, userID, orderID):
        info = self.orders.getOrderInfo(orderID)
        self.db.lrem("item:{}:{}".format(info["itemID"], info["type"]), orderID)
        if info["type"] == "buy":
            self.addBalance(userID, info["price"])
        else:
            self.moveItem("ADMIN", userID, info["itemID"])



    def getUserInfo(self, userID):
        return \
            {
                "name" : userID,
                "library" : self.getLibrary(userID),
                "inventory": self.getInventory(userID),
                "friends" : self.getFriendList(userID)
             }

