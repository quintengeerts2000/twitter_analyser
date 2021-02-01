import sqlite3
from Tweet import Tweet, Tweet_list

class Twitter_user:
    def __init__(self, name, handle):
        self.name = name
        self.handle = handle
        self.tweets = Tweet_list()
        self.Trades = list()

