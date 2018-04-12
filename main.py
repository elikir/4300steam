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


db = RedisDB.RedisDB()
messenger = RedisMessageAPI(db)
orders = RedisOrderAPI(db)
items = RedisItemAPI(db)
games = RedisGameAPI(db)
trades = RedisTradeAPI(db)
achievements = RedisAchievementAPI(db)
users = RedisUserAPI(db, messenger, orders, items, games, trades)






genres = RedisGenreAPI(db)


@app.route("/")
def homepage():
    db.reset()
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
    tradeID = users.makeTradeOffer("eli", "justin", ['1'], [])
    print tradeID
    return "ELI'S INVENTORY{} <br> ELI'S LIBRARY{}<br> JUSTIN'S INVENTORY{} <br> JUSTIN'S LIBRARY{}  <br> THEIR BALANCES NOW {} {}" .\
        format(users.getInventory("eli"), users.getLibrary("eli"), users.getInventory("justin"), users.getLibrary("justin"),
               users.getBalance("eli"), users.getTradeOffers("justin", "incoming"))











