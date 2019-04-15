from DataParser import dataParser
import tweepy

class SearchAPI:

    #   only the first 3000 tweets are available
    def getPreviousTweets(self, auth):
        api = tweepy.API(auth)
        for tweet in tweepy.Cursor(api.user_timeline, id='3237083798', tweet_mode='extended').items():
            data = dataParser()
            data.addToDB(tweet._json)