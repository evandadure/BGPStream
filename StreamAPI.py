# Import the necessary methods from tweepy library
from examples.streaming import StdOutListener
from tweepy.streaming import StreamListener
from DataParser import dataParser
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import tweepy
import json

# =============================================================================
# code inspiré de http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
# =============================================================================

# This is a basic listener that just prints received tweets to stdout.
class StreamAPI(StreamListener):

    def __init__(self):
        print("Listening through the Twitter Streaming API...")

    def on_data(self, data):
        tweet = json.loads(data)
        print(tweet)
        return True

    def on_error(self, status):
        print(status)

    def getNextTweets(self,auth):
        l = StdOutListener()
        stream = tweepy.Stream(auth=auth, listener=l)
        # stream.filter(track=["testttesthh"])
        stream.filter(follow=["818456674507902977"])





