from flask import Flask
app = Flask(__name__)


from APIs.RedisAPI.RedisUserAPI import RedisUserAPI
from APIs.RedisAPI.RedisGenreAPI import RedisGenreAPI
from APIs.RedisAPI.RedisAchievementAPI import RedisAchievementAPI
from APIs.RedisAPI.RedisGameAPI import RedisGameAPI
from APIs.RedisAPI.RedisItemAPI import RedisItemAPI
from APIs.RedisAPI.RedisMessageAPI import RedisMessageAPI
from APIs.RedisDB import RedisDB

db = RedisDB.RedisDB()
messenger = RedisMessageAPI(db)
users = RedisUserAPI(db, messenger)
games = RedisGameAPI(db)
items = RedisItemAPI(db)
achievements = RedisAchievementAPI(db)

genres = RedisGenreAPI(db)


@app.route("/")
def homepage():
    users.messageFriend("eli", "justin", "1v1 me on rust fgt")
    return "{}".format(users.getMessages("eli", "justin"))











