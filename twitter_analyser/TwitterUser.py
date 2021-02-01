import sqlite3
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

class TwitterUserList:
    def __init__(self):
        pass



class TwitterUserDA:
    def __init__(self):
        pass

    def save(self):
        pass

    def load(self):
        pass