import sqlite3
from pathlib import Path
from twitterscraper import User

from Tweet import Tweet, TweetList
from StockComment import StockComment, StockCommentList, StockCommentDA
from Trade import Trade, TradeList, TradeDA

class TwitterUser(User):
    def __init__(self, user="", full_name="", location="", blog="", date_joined="", id="", tweets=0, following=0,
                 followers=0, likes=0, lists=0, is_verified=0, saved_tweets=None, trades=None, stock_comments=None):

        User.__init__(self, user=user, full_name=full_name, location=location, blog=blog, date_joined=date_joined,
                      id=id, tweets=tweets, following=following, followers=followers, likes=likes, lists=lists,
                      is_verified=is_verified)

        if saved_tweets is not None:
            self.saved_tweets = saved_tweets
        else:
            self.saved_tweets = TweetList()
        if trades is not None:
            self.trades = trades
        else:
            self.trades = TradeList()
        if stock_comments is not None:
            self.stock_comments = stock_comments
        else:
            self.stock_comments = StockCommentList()

    def __str__(self):
        return 'Twitter user: name = {}, id = {}'.format(self.user, self.id)

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
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS TwitterUser (id string PRIMARY KEY, user string,
                full_name string, location string, blog string, date_joined string, tweets integer,following integer,
                followers integer, likes integer, lists integer, is_verified integer, saved_tweets integer, 
                trades integer, stock_comments integer)""")
        self.conn.commit()

    def save_user(self, usr):
        self.cursor = self.conn.cursor()
        data = (usr.id, usr.user, usr.full_name, usr.location, usr.blog, usr.date_joined, usr.tweets, usr.following,
                usr.followers, usr.likes, usr.lists, usr.is_verified, usr.saved_tweets.id, usr.trades.id,
                usr.stock_comments.id)
        self.cursor.execute('INSERT INTO TwitterUser VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
        self.conn.commit()

    def load_user(self, id=None, user=None):
        self.cursor = self.conn.cursor()
        if id is not None:
            out = self.cursor.execute('SELECT * FROM TwitterUser WHERE id = {}'.format(str(id))).fetchone()
            self.conn.commit()
        elif user is not None:
            out = self.cursor.execute("SELECT * FROM TwitterUser WHERE user = '{}'".format(user)).fetchone()
            self.conn.commit()
        else:
            raise ValueError("you need to use a name or id")
        return TwitterUser(out[1], out[2], out[3], out[4], out[5], out[0], out[6], out[7], out[8], out[9], out[10],
                           out[11], out[12], out[13], out[14])

    def save_list(self, user_list):
        DA = TwitterUserDA()
        for user in user_list.users:
            DA.save_user(user)

    def load_all(self):
        self.cursor = self.conn.cursor()
        query = self.cursor.execute('SELECT * FROM TwitterUser').fetchall()
        output = TwitterUserList("output")
        for entry in query:
            _ = TwitterUser(entry[1], entry[2], entry[3], entry[4], entry[5], entry[0], entry[6], entry[7], entry[8],
                            entry[9], entry[10], entry[11], entry[12], entry[13], entry[14])
            output.add_user(_)
        return output