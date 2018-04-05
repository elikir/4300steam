from APIs.API import UserAPI

class RedisUserAPI(UserAPI.UserAPI):

    db = None
    messenger = None

    def __init__(self, db, messenger):
        self.db = db
        self.messenger = messenger


    def addUser(self, userID, password):
        self.db.set(userID, password)
        self.db.set("user:{}:balance".format(userID), 0)

    def addGame(self,userID, gameID):
        key = "user:{}:library".format(userID)
        self.db.sadd(key, gameID)

    def addItem(self,userID, itemID):
        key = "user:{}:inventory".format(userID)
        self.db.sadd(key, itemID)

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
        return int(self.db.get(key))

    def getLibrary(self, userID):
        key = "user:{}:library".format(userID)
        return self.db.smembers(key)

    def getInventory(self, userID):
        key = "user:{}:inventory".format(userID)
        return self.db.smembers(key)

    def getFriendList(self, userID):
        key = "user:{}:friendList".format(userID)
        return self.db.smembers(key)

    def getMessages(self, userID, friendID):
        key = "user:{}:friend:{}:messages".format(userID, friendID)
        return [{"message" : self.messenger.getMessageContents(x),
                "from" : self.messenger.getMessageFrom(x),
                "to" : self.messenger.getMessageTo(x)}
                for x in self.db.lmembers(key)]