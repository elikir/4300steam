from APIs.API import MessageAPI

import string
import random

class RedisMessageAPI(MessageAPI.MessageAPI):

    db = None

    def __init__(self, db):
        self.db = db

    def sendMessage(self, fromUser, toUser, content):
        msg_uuid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        key1 = "message:{}:from".format(msg_uuid)
        key2 = "message:{}:to".format(msg_uuid)
        key3 = "message:{}:message".format(msg_uuid)

        self.db.set(key1, fromUser)
        self.db.set(key2, toUser)
        self.db.set(key3, content)

        return msg_uuid

    def getMessageContents(self, messageID):
        key = "message:{}:message".format(messageID)
        return self.db.get(key)

    def getMessageTo(self, messageID):
        key = "message:{}:to".format(messageID)
        return self.db.get(key)

    def getMessageFrom(self, messageID):
        key = "message:{}:from".format(messageID)
        return self.db.get(key)