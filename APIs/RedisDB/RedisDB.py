import redis


class RedisDB():

    db = None

    def __init__(self):
        self.db = redis.StrictRedis(host='localhost', port=6379, db=0)


    def get(self, key):
        return self.db.get(key)

    def set(self,key,value):
        self.db.set(key, value)


    def sadd(self, key, value):
        self.db.sadd(key,value)

    def smembers(self, key):
        return [x for x in self.db.smembers(key)]

    def lpush(self, key, value):
        self.db.lpush(key, value)

    def lmembers(self, key):
        return [x for x in self.db.lrange(key, 0, -1)]

    def ladd(self, key, values):
        for value in values:
            self.lpush(key, value)

    def reset(self):
        self.db.flushall()

    def exists(self, key):
        return self.db.exists(key)


    def lrem(self, key, value):
        self.db.lrem(key, 0, value)

    def delete(self, key):
        self.db.delete(key)

    def srem(self, key, values):
        for value in values:
            self.db.srem(key, value)