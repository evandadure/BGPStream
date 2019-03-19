#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json


#Variables that contains the user credentials to access Twitter API 
access_token = "1102669296709320708-kBmctssiSRU7AvvxBslcDihPS1BCIG"
access_token_secret = "coZiL3btq8EDGsaOJ34j89BIlDN11BtBERsODPChEqkL7"
consumer_key = "OGHehhsnT9WQL05ZgqlJ0RoNH"
consumer_secret = "E816Lpi1aW61vIq4eBWcMnj03fkD0HcmznyYx6jYwtoz15p1DC"


# =============================================================================
# code inspiré de http://adilmoujahid.com/posts/2014/07/twitter-analytics/
# =============================================================================

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        print(tweet)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(follow=['3237083798'])