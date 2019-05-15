from tweepy import OAuthHandler
from src.StreamAPI import StreamAPI
from src.SearchAPI import SearchAPI
import json


class Main():
    if __name__ == '__main__':
        # This handles Twitter authentication and the connection to Twitter API
        # The API Key Information are stored in data/keys.json
        with open('data/keys.json') as json_file:
            data = json.load(json_file)
        auth = OAuthHandler(data['consumer_key'], data['consumer_secret'])
        auth.set_access_token(data['access_token'], data['access_token_secret'])

        # Creates a new StreamAPI object and gets the incoming tweets
        streamAPI = StreamAPI()
        # streamAPI.getNextTweets(auth)

        # Creates a new SearchAPI object and gets the previous tweets
        searchAPI = SearchAPI()
        searchAPI.getPreviousTweets(auth)