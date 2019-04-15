from tweepy import OAuthHandler
from StreamAPI import StreamAPI
from SearchAPI import SearchAPI
import json


class Main():
    with open('data/keys.json') as json_file:
        data = json.load(json_file)
    if __name__ == '__main__':
        # This handles Twitter authetification and the connection to Twitter API
        auth = OAuthHandler(data['consumer_key'], data['consumer_secret'])
        auth.set_access_token(data['access_token'], data['access_token_secret'])
        streamAPI = StreamAPI()
        searchAPI = SearchAPI()
        # streamAPI.getNextTweets(auth)
        searchAPI.getPreviousTweets(auth)