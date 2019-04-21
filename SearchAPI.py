from DataParser import dataParser
import tweepy


class SearchAPI:

    def getPreviousTweets(self, auth):
        """
        Uses the Search API of tweepy to get all the previous tweets. Here we want only the tweets of BGPStream.
        Only the first 3000 tweets are available.
        ----------
        Parameters :
            - auth : the user's information (API keys)
        Returns :
            No return.
        """
        api = tweepy.API(auth)
        for tweet in tweepy.Cursor(api.user_timeline, id='3237083798', tweet_mode='extended').items():
            data = dataParser()
            data.addToDB(tweet._json)
