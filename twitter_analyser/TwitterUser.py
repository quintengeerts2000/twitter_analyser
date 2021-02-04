import sqlite3
from pathlib import Path
import hashlib

from Tweet import Tweet, TweetList
from StockComment import StockComment, StockCommentList, StockCommentDA
from Trade import Trade, TradeList, TradeDA

class TwitterUser:
    def __init__(self, username="", location="", description="", date_joined="", following='',
                 followers=0, saved_tweets=None, trades=None, stock_comments=None):
        self.username = username
        #generate unique id from hash function
        self.user_id = hashlib.sha1(str.encode(self.username)).hexdigest()
        self.location = location
        self.description = description
        self.date_joined = date_joined
        self.following = str(following)
        self.followers = str(followers)
        #initialise lists
        if saved_tweets is not None:
            self.saved_tweets = saved_tweets
        else:
            self.saved_tweets = TweetList(self.username)
        if trades is not None:
            self.trades = trades
        else:
            self.trades = TradeList()
        if stock_comments is not None:
            self.stock_comments = stock_comments
        else:
            self.stock_comments = StockCommentList()

    def __str__(self):
        return 'Twitter user: name = {}, id = {}'.format(self.username, self.user_id)

    def __eq__(self, other):
        return self.following == other.following and self.date_joined == other.date_joined and \
               self.description == other.description and self.username == other.username and \
               self.followers == other.followers and self.user_id == other.user_id


    def get_open_trades(self):
        pass

    def get_closed_trades(self):
        pass

    def get_performance(self):
        pass

class TwitterUserList:
    def __init__(self, name, users=None):
        self.name = name
        if users is not None:
            self.users = users
        else:
            self.users = list()

    def add_user(self, usr):
        self.users.append(usr)

    def remove_user(self, usr):
        self.users.remove(usr)

    def add_all_users(self, user_list):
        self.users.append(user_list)

    def __str__(self):
        out_str = ''
        for i in self.users:
            out_str += '\n' + str(i)
        return out_str

    def __getitem__(self, item):
        return self.users[item]


class TwitterUserDA:
    def __init__(self):
        path = Path(__file__).parents[1]
        directory = str(path)
        self.conn = sqlite3.connect(directory + '/sqlite_db/twitter_users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS TwitterUser (user_id string PRIMARY KEY, username string,
                location string, description string, date_joined string, following string, followers string)""")
        self.conn.commit()

    def save_user(self, usr):
        self.cursor = self.conn.cursor()
        data = (usr.user_id, usr.username, usr.location, usr.description, usr.date_joined, usr.following,
                usr.followers)
        self.cursor.execute('INSERT OR REPLACE INTO TwitterUser VALUES (?,?,?,?,?,?,?)', data)
        self.conn.commit()

    def load_user(self, id=None, username=None):
        self.cursor = self.conn.cursor()
        if id is not None:
            out = self.cursor.execute('SELECT * FROM TwitterUser WHERE user_id = {}'.format(str(id))).fetchone()
            self.conn.commit()
        elif username is not None:
            out = self.cursor.execute("SELECT * FROM TwitterUser WHERE username = '{}'".format(username)).fetchone()
            self.conn.commit()
        else:
            raise ValueError("you need to use a name or id")
        print(out)
        if out:
            return TwitterUser(username=out[1], location=out[2], description=out[3], date_joined=out[4],
                               following=out[5], followers=out[6])
        else:
            return None

    def save_list(self, user_list):
        DA = TwitterUserDA()
        for user in user_list.users:
            DA.save_user(user)

    def load_all(self):
        self.cursor = self.conn.cursor()
        query = self.cursor.execute('SELECT * FROM TwitterUser').fetchall()
        output = TwitterUserList("output")
        for entry in query:
            _ = TwitterUser(entry[1], entry[2], entry[3], entry[4], entry[5], entry[0], entry[6], entry[7], entry[8])
            output.add_user(_)
        return output