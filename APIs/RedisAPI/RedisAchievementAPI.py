from APIs.API import AchievementAPI

class RedisAchievementAPI(AchievementAPI.AchievementAPI):
    db = None

    def __init__(self, db):
        self.db = db

    def addAchievement(self, title, description):
        return NotImplementedError("Not implemented")

