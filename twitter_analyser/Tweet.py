import hashlib
import sqlite3
from pathlib import Path
import datetime as dt

class Tweet:
    def __init__(self, screen_name, username, user_id, timestamp, text, likes, retweets, emojis, comments, image_link,
                 URL):
        #id based on the text so if duplicates happen they have the same ID
        self.tweet_id = hashlib.sha1(str.encode(text)).hexdigest()
        #user id generated in the same way
        self.user_id = user_id
        self.screen_name = screen_name
        self.username = username
        self.timestamp = timestamp
        self.text = text
        self.emojis = emojis
        self.comments = comments
        self.likes = likes
        self.retweets = retweets
        self.image_link = image_link
        self.URL = URL

    def __str__(self):
        return "==========================================================================\n{}: {} * {} \n{}" \
               " \n--------------------------------------------------------------------------".format(self.screen_name,
                                                                                                      self.username,
                                                                                                      self.timestamp,
                                                                                                      self.text)

    def __eq__(self, other):
        for attr, value in self.__dict__.items():
            if value != eval('other.'+attr):
                print('not equal')
                return False
            return True

class TweetList:
    def __init__(self, name):
        self.name = name
        self.tweets = list()

    def add_tweet(self, tweet):
        self.tweets.append(tweet)

    def remove_tweet(self, tweet):
        self.tweets.remove(tweet)

    def __getitem__(self, item):
        return self.tweets[item]

    def __str__(self):
        string = ''
        for tweet in self:
            string += '\n' + str(tweet)
        return string

    def __eq__(self, other):
        for i, twt in enumerate(self):
            if twt != other[i]:
                return False
        return True

class TweetDA:
    def __init__(self):
        path = Path(__file__).parents[1]
        directory = str(path)
        self.conn = sqlite3.connect(directory + '/sqlite_db/tweets.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tweets (tweet_id string PRIMARY KEY, screen_name string , 
        username string, user_id string, timestamp string, text string, likes integer, retweets integer, emojis string,
        comments integer, image_link string, URL string)""")
        self.conn.commit()

    def save_tweet(self, twt):
        self.cursor = self.conn.cursor()
        data = (twt.tweet_id, twt.screen_name, twt.username, twt.user_id, twt.timestamp, twt.text,
                twt.likes, twt.retweets, twt.emojis, twt.comments, twt.image_link, twt.URL)
        self.cursor.execute('INSERT OR REPLACE INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', data)
        self.conn.commit()

    def load_tweet(self, id=None):
        self.cursor = self.conn.cursor()
        if id is not None:
            out = self.cursor.execute("SELECT * FROM tweets WHERE tweet_id = '{}'".format(str(id))).fetchone()
            self.conn.commit()
        else:
            raise ValueError("you need to give id")
        #Tweet ID is determined from the text so it doesnt have to be passed
        return Tweet(screen_name=out[1], username=out[2], user_id=out[3], timestamp=out[4],
                     text=out[5], likes=out[6], retweets=out[7], emojis=out[8], comments=out[9], image_link=out[10],
                     URL=out[11])

    def user_has_tweets(self, username):
        """
        checks whether a user already has tweets in the DB
        :param username: e.g @POTUS
        :return: True (if exists), False (if not)
        """
        self.cursor = self.conn.cursor()
        out = self.cursor.execute("""SELECT EXISTS(SELECT 1 FROM tweets WHERE username = '{}')""".format(username)).fetchone()
        if out[0] == 1:
            return True
        else:
            return False

    def get_last_entry_date(self, username):
        twts = self.load_all(username=username)
        last_date = dt.datetime(100, 1, 1)
        for twt in twts:
            date = dt.datetime.strptime(twt.timestamp, '%Y-%m-%dT%H:%M:%S.000Z')
            if date > last_date:
                last_date = date
        return last_date

    def save_list(self, twt_list):
        DA = TweetDA()
        for twt in twt_list:
            DA.save_tweet(twt)

    def load_all(self, screen_name=None, username=None):
        self.cursor = self.conn.cursor()
        output = TweetList("output")
        if screen_name is not None:
            query = self.cursor.execute("SELECT * FROM tweets WHERE screen_name = '{}'".format(screen_name)).fetchall()
        elif username is not None:
            query = self.cursor.execute("SELECT * FROM tweets WHERE username = '{}'".format(username)).fetchall()
        for out in query:
            _ = Tweet(screen_name=out[1], username=out[2], user_id=out[3], timestamp=out[4], text=out[5], likes=out[6],
                      retweets=out[7], emojis=out[8], comments=out[9], image_link=out[10], URL=out[11])
            output.add_tweet(_)
        return output

DA = TweetDA()
print(DA.load_all(username='@traderstewie'))