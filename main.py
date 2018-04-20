from flask import Flask, session, request, redirect, url_for
import flask_login
app = Flask(__name__)
app.secret_key = "JOHNRACHLIN"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


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
genres = RedisGenreAPI(db)
users = RedisUserAPI(db, messenger, orders, items, games, trades)



@app.route("/")
def homepage():
    return str(isLoggedIn())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = request.form['username']
    if users.validLogon(username, request.form['password']):
        loginUser(username)
        return "Logged in as " + username

    return 'Bad login'



def loginUser(username):
    db.set("logged_in_user", username)
    db.set("logged_in", 1)

def logout():
    db.delete("logged_in_user")
    db.set("logged_in", 0)

def isLoggedIn():
    return bool(int(db.get("logged_in")))
