import twitterscraper as ts

class TwitterScraper:
    def __init__(self):
        pass

from Scweet.scweet import scrap
data = scrap(start_date="2018-01-01", max_date="2018-01-05", from_account="traderstewie",interval=1,
      headless=True, display_type="image", hashtag=None, save_images=False)