import hashlib
import sqlite3
from pathlib import Path
import datetime as dt

class Tweet:
    def __init__(self, screen_name, username, user_id, timestamp, text, likes, retweets, emojis, comments, image_link,
                 URL, is_reply=None, is_reply_to=''):
        """
        :param screen_name: same as username
        :param username:
        :param user_id: twitter id
        :param timestamp: format: "YYYY-MM-DDThh:mm:ss.000Z:"
        :param text: body of the tweet
        :param likes: amount of likes
        :param retweets: amount of retweets
        :param emojis: the emojis in the tweet
        :param comments: amount of comments
        :param image_link: if it contains an image this is the link
        :param URL: url of the tweet
        :param is_reply: if the tweet was a reply
        :param is_reply_to: if it was a reply then to whom
        """
        #id based on the text so if duplicates happen they have the same ID
        self.tweet_id = str(hashlib.sha1(str.encode(str(text))).hexdigest())
        #user id generated in the same way
        self.user_id = user_id
        self.screen_name = screen_name
        self.username = username
        self.timestamp = timestamp
        self.is_reply_to = is_reply_to
        if is_reply is None:
            if "Replying to" in text:
                self.is_reply = True
                text = text.replace("Replying to", "")
                for i, t in enumerate(text.split()):
                    if t.startswith('@') and i == 0:
                        self.is_reply_to = t
            else:
                self.is_reply = False
                self.is_reply_to = ''
        else:
            self.is_reply = is_reply
            self.is_reply_to = is_reply_to
        self.text = text
        self.emojis = emojis
        self.comments = comments
        self.likes = likes
        self.retweets = retweets
        self.image_link = image_link
        self.URL = URL

    def __str__(self):
        if not self.is_reply:
            string = """==========================================================================
{}: {} * {}
{}
--------------------------------------------------------------------------""".format(self.screen_name,
                                                                                     self.username, self.timestamp,
                                                                                     self.text)
        else:
            string = """==========================================================================
{}: {} * {}
is reply to: {}
{}
--------------------------------------------------------------------------""".format(self.screen_name, self.username,
                                                                                     self.timestamp, self.is_reply_to,
                                                                                     self.text)
        return string


    def __eq__(self, other):
        for attr, value in self.__dict__.items():
            if value != eval('other.'+attr):
                print('not equal')
                return False
            return True

class TweetList:
    def __init__(self, name):
        """
        used to store multiple tweets
        :param name:
        """
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
        """
        used to store tweet and tweetlist objects
        """
        path = Path(__file__).parents[1]
        directory = str(path)
        #connect to the db
        self.conn = sqlite3.connect(directory + '/sqlite_db/tweets.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tweets (tweet_id string PRIMARY KEY, screen_name string , 
        username string, user_id string, timestamp string, text string, likes integer, retweets integer, emojis string,
        comments integer, image_link string, URL string, is_reply bool, is_reply_to string)""")
        self.conn.commit()

    def save_tweet(self, twt):
        self.cursor = self.conn.cursor()
        data = (twt.tweet_id, twt.screen_name, twt.username, twt.user_id, twt.timestamp, twt.text,
                twt.likes, twt.retweets, twt.emojis, twt.comments, twt.image_link, twt.URL, twt.is_reply,
                twt.is_reply_to)
        self.cursor.execute('INSERT OR REPLACE INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
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
                     URL=out[11], is_reply=out[12], is_reply_to=out[13])

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
        """
        returns the last tweet in the db for a given user
        :param username: handle
        :return: format: date in format:"YYYY-MM-DDThh:mm:ss.000Z"
        """
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

    def load_all(self, username=None, screen_name=None, replies=False):
        self.cursor = self.conn.cursor()
        output = TweetList("output")
        if screen_name is not None:
            query = self.cursor.execute("SELECT * FROM tweets WHERE screen_name = '{}' AND is_reply = {}".format(
                screen_name, replies)).fetchall()
        elif username is not None:
            query = self.cursor.execute("SELECT * FROM tweets WHERE username = '{}' AND is_reply = {}".format(
                username, replies)).fetchall()
        for out in query:
            _ = Tweet(screen_name=out[1], username=out[2], user_id=out[3], timestamp=out[4], text=out[5], likes=out[6],
                      retweets=out[7], emojis=out[8], comments=out[9], image_link=out[10], URL=out[11], is_reply=out[12],
                      is_reply_to=out[13])
            output.add_tweet(_)
        return output

