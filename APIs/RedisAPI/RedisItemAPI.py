from APIs.API import ItemAPI

class RedisItemAPI(ItemAPI.ItemAPI):

    db = None

    def __init__(self, db):
        self.db = db

    def addItem(self, name, gameId, description, imageLink):
        return NotImplementedError("Not implemented")
