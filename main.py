from flask import Flask
app = Flask(__name__)


from APIs.RedisAPI.RedisUserAPI import RedisUserAPI
from APIs.RedisAPI.RedisGenreAPI import RedisGenreAPI
from APIs.RedisAPI.RedisAchievementAPI import RedisAchievementAPI
from APIs.RedisAPI.RedisGameAPI import RedisGameAPI
from APIs.RedisAPI.RedisItemAPI import RedisItemAPI
from APIs.RedisAPI.RedisMessageAPI import RedisMessageAPI
from APIs.RedisDB import RedisDB
from APIs.RedisAPI.RedisOrderAPI import RedisOrderAPI
from APIs.RedisAPI.RedisTradeAPI import RedisTradeAPI
from APIs.RedisAPI.RedisTransactionAPI import RedisTransactionAPI

db = RedisDB.RedisDB()
messenger = RedisMessageAPI(db)
orders = RedisOrderAPI(db)
games = RedisGameAPI(db)
trades = RedisTradeAPI(db)
achievements = RedisAchievementAPI(db)
market = RedisTransactionAPI(db)
items = RedisItemAPI(db, orders, market)
users = RedisUserAPI(db, messenger, orders, items, games, trades)






genres = RedisGenreAPI(db)


@app.route("/")
def homepage():
    db.reset()
    users.addUser("ADMIN", "PASSWORD")
    users.addUser("eli", "e")
    users.addUser("justin", "j")
    users.addBalance("eli", 20)
    users.addBalance("justin", 19.98)
    games.addGame("1", "Counter Strike: Global Offensive", "FPS", 19.99, "A first person shooter", [])
    items.addItem("1", "AWP Dragon Lore", "1", "A 1 shot rifle boi", "")
    users.addItem("eli", "1")
    users.buyGame("eli", "1")
    users.buyGame("justin", "1")
    users.messageFriend("eli", "justin", "1v1 me on rust boi")
    users.messageFriend("justin", "eli", "but the CIA is watching me")
    users.makeSellOrder("eli", "1", 15)
    users.makeBuyOrder("justin", "1", 14.99)
    orders = users.getOrders("justin", "buy")
    users.cancelOrder("justin", orders[0])
    print users.getBalance("justin")
    return "hello world"











