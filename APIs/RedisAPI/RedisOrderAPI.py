from APIs.API import OrderAPI

import string
import random

class RedisOrderAPI(OrderAPI.OrderAPI):

    db = None

    def __init__(self, db):
        self.db = db


    def makeOrder(self, type, userID, itemID, price):
        uuid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

        key1 = "order:{}:type".format(uuid)
        key2 = "order:{}:userID".format(uuid)
        key3 = "order:{}:itemID".format(uuid)
        key4 = "order:{}:price".format(uuid)
        self.db.set(key1, type)
        self.db.set(key2, userID)
        self.db.set(key3, itemID)
        self.db.set(key4, price)

        return uuid

