from Tweet import *
from TwitterUser import *
from Scweet.scweet import scrap
import hashlib
import os.path
import os
import pandas as pd
from Scweet.user import get_user_information
from Scweet.utils import get_last_date_from_csv
import datetime as dt

class TwitterScraper:
    def __init__(self, username):
        #create a list to store the tweets
        self.tweets = TweetList('{}'.format(username))
        self.username = username
        self.user = TwitterUserDA().load_user(user=username)
        if self.user is None:
            self.check_user_info()

    def get_tweets(self, start, end, resume=False):
        scrap(start_date=start, max_date=end, from_account=self.user.user, interval=5,
              headless=True, display_type="Top", hashtag=None, save_images=False, show_images=False, resume=resume)

    def check_user_info(self):
        out = get_user_information([self.username], headless=True)
        info = out[self.username]
        following = info[0]
        followers = info[1]
        join_date = info[2]
        birthdate = info[3]
        location = info[4]
        website = info[5]
        description = info[6]
        hash = hashlib.sha1(str.encode(self.username)).hexdigest()
        self.user = TwitterUser(user=self.username, location=location, blog=description, id=hash,
                                followers=followers, following=following, date_joined=join_date)
        # save this user
        TwitterUserDA().save_user(self.user)

    def _parse_csv(self, fname):
        #TODO: finish method
        #create function to help with converting the csv to a tweetlist
        df = pd.read_csv(fname)
        #create a tweetlist from this file
        for i, row in df.iterrows():
            twt = Tweet(row['UserScreenName', row['UserName'], )
            screen_name, username, user_id, tweet_id, tweet_url, timestamp, timestamp_epochs, text,
            text_html, links, hashtags, has_media, img_urls, video_url, likes, retweets, replies, is_replied,
            is_reply_to, parent_tweet_id, reply_to_users)
            self.tweets.add_tweet()
        pass

    def create_database(self):
        #check if user already has tweets in DB
        DA = TweetDA()
        if DA.user_has_tweets(self.username):
            #if he has tweets get the last tweet entry in the DB
            start = DA.get_last_entry_date(self.username)
            #add 10 days
            end = (start + dt.timedelta(days=10)).strftime('%Y-%m-%d')
            #form string
            start = start.strftime('%Y-%m-%d')
        else:
            # find the date to start
            string = str(self.user.date_joined).replace("Joined ", "")
            start = dt.datetime.strptime(string, '%B %Y')
            end = (start + dt.timedelta(days=10)).strftime('%Y-%m-%d')
            start = start.strftime('%Y-%m-%d')
            # find the date to end
        final_date = dt.datetime.today()
        working = True
        while working:
            #get the tweets
            self.get_tweets(start, end, resume=False)
            fname = '/outputs/{}_{}_{}.csv'.format(self.username, start, end) #name of file
            #turn the csv to tweetlist
            twts = self._parse_csv(fname)
            #save the tweetlist in the db
            DA.save_list(twts)
            #delete the csv
            os.remove(fname)
            #create new start and end dates
            start = end
            end = (dt.datetime.strptime(start, '%Y-%m-%d') + dt.timedelta(days=10)).strftime('%Y-%m-%d')
            # check if we need a new iteration
            working = dt.datetime.strptime(end, '%Y-%m-%d') < final_date

        
print(a.columns)
print(a.UserScreenName)
print(a.UserName)
print(a.Timestamp)
print(a.Text)
print(a.Emojis)
print(a.Comments)
print(a.Likes)
print(a.Retweets)
print(a['Image link'])
print(a['Tweet URL'])

print(TweetDA().load_all('quinten'))