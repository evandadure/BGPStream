#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import tweepy
import json

with open('data/keys.json') as json_file:
    data = json.load(json_file)

# =============================================================================
# code inspiré de http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
# =============================================================================

#This is a basic listener that just prints received tweets to stdout.
class TwitterListener(StreamListener):

    def __init__(self):
        print("commence")

    def on_data(self, data):
        tweet = json.loads(data)
        print(tweet)
        return True

    def on_error(self, status):
        print(status)
        
        
#   only the first 3000 tweets are available
    def getPreviousTweets(self):
        api = API(auth)
        tweets = []
        for tweet in tweepy.Cursor(api.user_timeline,id='3237083798').items():
            tweets.append(tweet._json)
        return tweets[0]


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = TwitterListener()
    auth = OAuthHandler(data['consumer_key'], data['consumer_secret'])
    auth.set_access_token(data['access_token'], data['access_token_secret'])
#    stream = Stream(auth, l)
#
#    stream.filter(track=['poule'])

    print(l.getPreviousTweets())
    #stream.filter(follow=['3237083798'])