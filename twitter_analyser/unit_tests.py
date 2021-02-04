import unittest
#import internal packages
from TwitterUser import *
from Tweet import *
from TwitterScraper import *

class TwitterUserTests(unittest.TestCase):

    def test_save_and_load_multiple_users(self):
        usr1 = TwitterUser('@SCOTUS', 'white house', 'president of the united states', 'June 2009', '14k', '120')
        usr2 = TwitterUser('@FLOTUS', 'white house', 'first lady of the united states', 'June 2010', '1k', '30')
        group = TwitterUserList('white house')
        group.add_user(usr1)
        group.add_user(usr2)
        DA = TwitterUserDA()
        DA.save_list(group)
        load_group = DA.load_all()
        #self.assertEqual(group, load_group)

    def test_save_and_load_user(self):
        usr = TwitterUser('@POTUS', 'white house', 'president of the united states', 'June 2009', '14k', '120')
        DA = TwitterUserDA()
        #save
        DA.save_user(usr)
        #load
        load_usr = DA.load_user(username='@POTUS')
        self.assertEqual(usr, load_usr)

class TweetTests(unittest.TestCase):
    def test_save_and_load_tweet(self):
        usr = TwitterUser('@POTUS', 'white house', 'president of the united states', 'June 2009', '14k', '120')
        twt = Tweet('Donald Trump', usr.username, usr.user_id, '2020-02-01T06:33:23.000Z', 'Rocketman!', 120, 3929, '',
                    300, 'image url', 'URL')

        DA = TweetDA()
        DA.save_tweet(twt)
        load_twt = DA.load_tweet(twt.tweet_id)
        self.assertEqual(twt, load_twt)

    def test_save_and_load_multiple_tweets(self):
        usr = TwitterUser('@POTUS', 'white house', 'president of the united states', 'June 2009', '14k', '120')
        twt1 = Tweet('Donald Trump', usr.username, usr.user_id, '2020-02-01T06:33:23.000Z', 'Rocketman!', 120, 3929, '',
                     300, 'image url', 'URL')
        twt2 = Tweet('Donald Trump', usr.username, usr.user_id, '2020-03-01T08:33:23.000Z', 'NO!', 120, 3929, '',
                     300, 'image url', 'URL')
        twt_list = TweetList('donny')
        twt_list.add_tweet(twt1)
        twt_list.add_tweet(twt2)
        DA = TweetDA()
        DA.save_list(twt_list)
        load_list = DA.load_all(username='@POTUS')
        self.assertEqual(twt_list, load_list)

class TwitterScraperTests(unittest.TestCase):
    def test_create_database(self):
        #check if it can find the account
        scraper = TwitterScraper('@traderstewie')
        scraper.date_joined = 'Januari 2021'
        scraper.create_database()

if __name__ == '__main__':
    unittest.main()
