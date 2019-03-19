#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

with open('data/keys.json') as json_file:
    data = json.load(json_file)

# =============================================================================
# code inspiré de http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
# =============================================================================

#This is a basic listener that just prints received tweets to stdout.
class TwitterListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        print(tweet)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = TwitterListener()
    auth = OAuthHandler(data['consumer_key'], data['consumer_secret'])
    auth.set_access_token(data['access_token'], data['access_token_secret'])
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(follow=['3237083798'])