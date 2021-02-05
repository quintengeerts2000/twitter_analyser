from Tweet import *
from TwitterUser import *
import TwitterAPI as Tapi
from Scweet.scweet import scrap
import hashlib
import os.path
import os
import pandas as pd
from Scweet.user import get_user_information
from Scweet.utils import get_last_date_from_csv
import datetime as dt
from constants import cons_key, cons_secret, token, token_secret



class TwitterScraper:
    def __init__(self, username):
        #create a list to store the tweets
        self.tweets = TweetList('{}'.format(username))
        self.username = username.replace('@', '')
        self.user = TwitterUserDA().load_user(username=username)
        if self.user is None:
            self.check_user_info()

    def get_tweets(self, start, end, resume=False):
        scrap(start_date=start, max_date=end, from_account=self.username, interval=5,
              headless=True, display_type="Top", hashtag=None, save_images=False, show_images=False, resume=resume)

    def check_user_info(self):
        """
        Searches for twitter user profile and saves the data
        :return:
        """
        api = Tapi.TwitterAPI(cons_key, cons_secret, token, token_secret)
        out = api.request('users/lookup', {'Name': '{}'.format(self.username), 'screen_name': '{}'.format(self.username)})
        if out is not None:
            for i in out:
                info = i
            following = info['friends_count']
            followers = info['followers_count']
            join_date = info['created_at']
            location = info['location']
            description = info['description']
            user_id = info['id_str']
            self.user = TwitterUser(username=info['screen_name'], location=location, description=description,
                                    date_joined=join_date, following=following, followers=followers,id=user_id)
            # save this user
            TwitterUserDA().save_user(self.user)
        else:
            self.user = TwitterUser(username=self.username, location="", description="*manually created*",
                                    date_joined="Joined June 2009", following='', followers='')

    def _parse_csv(self, fname):
        #create function to help with converting the csv to a tweetlist
        df = pd.read_csv(fname)
        tweets = TweetList('output')
        #create a tweetlist from this file
        for i, row in df.iterrows():
            twt = Tweet(row['UserScreenName'], row['UserName'], self.user.user_id, row['Timestamp'], row['Text'],
                            row['Likes'], row['Retweets'], row['Emojis'], row['Comments'], row['Image link'],
                            row['Tweet URL'])
            tweets.add_tweet(twt)
        return tweets

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
            start = dt.datetime.strptime(self.user.date_joined, '%a %b %d %H:%M:%S +0000 %Y')
            end = (start + dt.timedelta(days=10)).strftime('%Y-%m-%d')
            start = start.strftime('%Y-%m-%d')
            # find the date to end
        final_date = dt.datetime.today()
        working = True
        while working:
            #get the tweets
            self.get_tweets(start, end, resume=False)
            fname = 'outputs/{}_{}_{}.csv'.format(self.username, start, end) #name of file
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

class DBcreator:
    def __init__(self):
        pass


if __name__ == '__main__':
    #list of twitter users I want to scrape:
    users_to_scrape = ['traderstewie', 'jmoneystonks', 'Thrackx', 'thetradejourney', 'TraderAmogh', 'JackDamn',
                       'Scelliott81']
    for usr in users_to_scrape:
        print("\n+++++++++++++++++++++{}++++++++++++++++++++++++".format(usr + ' starting') * 100)
        TwitterScraper(usr).create_database()
        print("\n+++++++++++++++++++++{}++++++++++++++++++++++++".format(usr + ' finished')*100)
