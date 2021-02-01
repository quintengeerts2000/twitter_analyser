import sqlite3
from pathlib import Path

from Tweet import Tweet, TweetList
from StockComment import StockComment, StockCommentList, StockCommentDA
from Trade import Trade, TradeList, TradeDA

class TwitterUser:
    def __init__(self, name, handle, tweets=None, trades=None, stock_comments=None):
        self.name = name
        self.handle = handle
        if tweets is not None:
            self.tweets = tweets
        else:
            self.tweets = TweetList()
        if trades is not None:
            self.trades = trades
        else:
            self.trades = TradeList()
        if stock_comments is not None:
            self.stock_comments = stock_comments
        else:
            self.stock_comments = StockCommentList()

    def get_open_trades(self):
        pass

    def get_closed_trades(self):
        pass

    def get_performance(self):
        pass




class TwitterUserList:
    def __init__(self):
        pass



class TwitterUserDA:
    def __init__(self):
        path = Path()
        directory = str(path.parent.parent)
        self.conn = sqlite3.connect(directory + '/DataBase')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS TwitterUser (timestamp integer PRIMARY KEY, best_bid real,
                best_ask real, avg_buy integer, avg_sell integer, quantity_buy real, quantity_sell real)""")
        self.conn.commit()
        pass

    def save(self):
        pass

    def load(self):
        pass

if __name__ == "__main__":
    path = Path()
    print(path.absolute())
    print(type(str(path.parent.parent)))