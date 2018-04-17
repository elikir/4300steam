from APIs.API import TransactionAPI

import string
import random
import time
import datetime


class RedisTransactionAPI(TransactionAPI.TransactionAPI):
    db = None

    def __init__(self, db):
        self.db = db

    def makeTransaction(self, itemID, price):
        uuid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        key1 = "transaction:{}:itemID".format(uuid)
        key2 = "transaction:{}:price".format(uuid)
        key3 = "transaction:{}:stamp".format(uuid)
        self.db.set(key1, itemID)
        self.db.set(key2, price)
        self.db.set(key3, st)
        return uuid

    def getTransactionInfo(self, transactionID):
        key1 = "transaction:{}:itemID".format(transactionID)
        key2 = "transaction:{}:price".format(transactionID)
        key3 = "transaction:{}:stamp".format(transactionID)

        return {"item": self.db.get(key1),
                "price": self.db.get(key2),
                "stamp": self.db.get(key3)
                }
