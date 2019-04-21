from tweepy.streaming import StreamListener
from DataParser import dataParser
import tweepy
import json

# =============================================================================
# Code inspired by http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
# =============================================================================

# This is a basic listener that just prints received tweets to stdout.
class StreamAPI(StreamListener):

    def __init__(self):
        """
        Initialize the StreamAPI and prints a phrase.
        ----------
        Parameters :
            No parameter.
        Returns :
            No return.
        """
        print("Listening through the Twitter Streaming API...")

    def on_data(self, data):
        """
        Whenever BGPStream tweets something, this tweet is parsed and added to the database automatically with this
        method.
        ----------
        Parameters :
            - data(str) : the JSON text containing all the tweet information.
        Returns :
            - True : default return for the on_data method of the StreamListener class
        """
        # creates the dataParser
        parser = dataParser()
        tweet = json.loads(data)
        # gets the needed information from the tweet (text, creation date, id of the tweet)
        tweet_content = self.getTweetContent(tweet)
        # adds the parsed tweet in the database
        parser.addToDB(tweet_content)
        print(tweet_content)
        return True

    def on_error(self, status):
        """
        Prints an error message when an error occurs.
        ----------
        Parameters :
            - status : some information about the error
        Returns :
            No return.
        """
        print("ERROR : Something wrong happened.")
        print(status)
        pass

    def getNextTweets(self,auth):
        """
        Uses the Stream API of tweepy to get all the incoming tweets. Here we want only the tweets of BGPStream.
        ----------
        Parameters :
            - auth : the user's information (API keys)
        Returns :
            No return.
        """
        stream = tweepy.Stream(auth=auth, listener=self, tweet_mode='extended')
        # Filters only the tweets of BGPStream
        # stream.filter(follow=["3237083798"])
        stream.filter(follow=["3237083798"])

    def getTweetContent(self, tweetJson):
        """
        This method is useful only because the structure of the tweet's information JSON of a tweet found with the
        "Search" API is slightly different from the one of a tweet found with the "Stream" API. Indeed, for the "Stream"
        API, if the tweet's text exceeds 141 characters, this text will be truncated.
        ----------
        Parameters :
            - tweetJson : all information from a specific tweet
        Returns :
            - useful_content : a dictionary containing only the information needed for our database (this information
            will be treated exactly as a tweet found with the Search API)
        """
        # If the tweet's text extends 141 characters, the full text is displayed in "extented_tweet" part of the JSON.
        useful_content = {}
        if("extended_tweet" in tweetJson):
            useful_content["full_text"] = tweetJson["extended_tweet"]["full_text"]
        else:
            useful_content["full_text"] = tweetJson["text"]
        useful_content["created_at"] = tweetJson["created_at"]
        useful_content["id_str"] = tweetJson["id_str"]
        return useful_content
