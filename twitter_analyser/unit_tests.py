import unittest
#import internal packages
from TwitterUser import *
from Tweet import *

class TwitterUserTests(unittest.TestCase):
    def test_save_and_load_user(self):
        usr = TwitterUser('@POTUS', 'white house', 'president of the united states', 'June 2009', '14k', '120')
        DA = TwitterUserDA()
        #save
        DA.save_user(usr)
        #load
        load_usr = DA.load_user(username='@POTUS')
        self.assertEqual(usr, load_usr)


class TweetTests(unittest.TestCase):
    # TODO: create unittests for all the classes and methods
    pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TwitterUserTests('save_and_load_user_test'))
    return suite

if __name__ == '__main__':
    unittest.main()

