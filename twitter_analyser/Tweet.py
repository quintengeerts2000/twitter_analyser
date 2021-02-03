from twitterscraper import Tweet as Tw
import uuid
import sqlite3
from pathlib import Path

class Tweet(Tw):
    def __init__(self, screen_name, username, user_id, tweet_id, tweet_url, timestamp, timestamp_epochs, text,
                 text_html, links, hashtags, has_media, img_urls, video_url, likes, retweets, replies, is_replied,
                 is_reply_to, parent_tweet_id, reply_to_users):

        Tw.__init__(self, screen_name=screen_name, username=username, user_id=user_id, tweet_id=tweet_id,
                    tweet_url=tweet_url, timestamp=timestamp, timestamp_epochs=timestamp_epochs,
                    text=text, text_html=text_html, links=links, hashtags=hashtags, has_media=has_media,
                    img_urls=img_urls, video_url=video_url, likes=likes, retweets=retweets, replies=replies,
                    is_replied=is_replied, is_reply_to=is_reply_to, parent_tweet_id=parent_tweet_id,
                    reply_to_users=reply_to_users)

    def __str__(self):
        return "Tweet(username = {}, timestamp = {})".format(self.username, self.timestamp)

class TweetList:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
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

class TweetDA:
    def __init__(self):
        path = Path(__file__).parents[1]
        directory = str(path)
        self.conn = sqlite3.connect(directory + '/sqlite_db/tweets.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Tweets (screen_name string , username string,
        user_id string, tweet_id string PRIMARY KEY, tweet_url string, timestamp string, timestamp_epochs string, 
        text string, text_html string, links string, hashtags string, has_media string, img_urls string,
        video_url string, likes integer, retweets integer, replies integer, is_replied string,
                 is_reply_to string, parent_tweet_id string, reply_to_users string)""")
        self.conn.commit()

    def save_tweet(self, twt):
        self.cursor = self.conn.cursor()
        data = (twt.screen_name, twt.username, twt.user_id, twt.tweet_id, twt.tweet_url, twt.timestamp,
                twt.timestamp_epochs, twt.text, twt.text_html, twt.links, twt.hashtags, twt.has_media, twt.img_urls,
                twt.video_url, twt.likes, twt.retweets, twt.replies, twt.is_replied, twt.is_reply_to,
                twt.parent_tweet_id, twt.reply_to_users)
        self.cursor.execute('INSERT INTO Tweets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
        self.conn.commit()

    def load_tweet(self, id=None):
        self.cursor = self.conn.cursor()
        if id is not None:
            out = self.cursor.execute('SELECT * FROM tweets WHERE tweet_id = {}'.format(str(id))).fetchone()
            self.conn.commit()
        else:
            raise ValueError("you need to give id")
        return Tweet(out[0], out[1], out[2], out[3], out[4], out[5], out[6], out[7], out[8], out[9], out[10], out[11],
                     out[12], out[13], out[14], out[15], out[16], out[17], out[18], out[19], out[20])

    def save_list(self, twt_list):
        DA = TweetDA()
        for twt in twt_list:
            DA.save_tweet(twt)

    def load_all(self, screen_name):
        self.cursor = self.conn.cursor()
        output = TweetList("output")
        query = self.cursor.execute("SELECT * FROM tweets WHERE screen_name = '{}'".format(screen_name)).fetchall()
        for out in query:
            _ = Tweet(out[0], out[1], out[2], out[3], out[4], out[5], out[6], out[7], out[8], out[9], out[10], out[11],
                      out[12], out[13], out[14], out[15], out[16], out[17], out[18], out[19], out[20])
            output.add_tweet(_)
        return output
