# -*- coding: utf-8 -*-

# TO DO :
# - écrire dans le rapport qu'avec notre schéma, on peut rechercher d'autres mots clés à partir d'un mot clé d'un tweet (en regardant son contenu)




# Import the necessary package to process data in JSON format
import mysql.connector
import tweepy
import coords
import tokenizer
from datetime import datetime, timedelta
try:
    import json
except ImportError:
    import simplejson as json












# Variables that contains the user credentials to access Twitter API

# ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
# ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
# CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
# CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

ACCESS_TOKEN = '818456674507902977-CweXH1SJkOeyKLAc1EUnZ2JKSHpC83Z'
ACCESS_SECRET = 'kLla8weNLy1tfEdwEIlUmz9g1tV91sO7VHE5dOhyrYLsL'
CONSUMER_KEY = '5HmCS4zWFTa47hJHa3KKOknDE'
CONSUMER_SECRET = 'pMKmFuHeY5Xzo4LOcGQIxCSo18GALolGfn927p5cKjpWeRMxWI'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


# CONNECTION TO THE DATABASE
# =============================================================================
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="tp_twitterosm"
)
mycursor = mydb.cursor()
# =============================================================================


def setDateTime(dateTweet):
    """
    Fonction qui crée un datetime à partir d'une string de date (exemple "21/08/18"), et d'une string d'heure (exemple "13:37")
    Parametres :
        - date : String de la date
        - heure : String de l'heure
    Retourne :
        d : la date (et son heure) dans le type datetime
    """
    monthsDic  = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    dateToString = dateTweet[8:10]+"/"+monthsDic[dateTweet[4:7]]+"/"+dateTweet[-2:]
    d = datetime.strptime(dateToString,"%d/%m/%y")
    h = dateTweet[dateTweet.find(':')-2:dateTweet.find(':')]
    m = dateTweet[dateTweet.find(':')+1:dateTweet.find(':')+3]
    d = d.replace(hour=int(h),minute=int(m))
    d = d + timedelta(hours=1)
    return d

# METHODES DE TRAITEMENT DES LONGITUDES/LATITUDES AFFICHEES DANS UN TWEET
# Ces méthodes font la moyennes des valeurs du "polygone" de la localisation d'un tweet
# =============================================================================
def getLongAndLat(listeCouplesCoord):
    listeLongitude = []
    listeLatitude = []
    for couple in listeCouplesCoord:
        listeLongitude.append(couple[0])
        listeLatitude.append(couple[1])
    return (listeLongitude,listeLatitude)

def moyList(list):
    return (sum(list)/len(list))


def centrePolygone(list_Longitude, list_Latitude):
    return [moyList(list_Longitude), moyList(list_Latitude)]


def get_trends(WOEID):
    trends1 = api.trends_place(WOEID) # WOEID of Paris : 615702
    # trends1 is a list with only one element in it, which is a
    # dict which we'll put in data.
    data = trends1[0]
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends]
    return names


def addTweet(created_at, text, user_id, user_name, screen_name, latitude, longitude, searched_keyword, nearest_city, numero_tweet):
    sql = "INSERT INTO tweet (created_at, text, user_id, user_name, screen_name, \
        latitude, longitude, searched_keyword, nearest_city, numero_tweet) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (created_at, text, user_id, user_name, screen_name, latitude, longitude, searched_keyword, nearest_city, numero_tweet)
    mycursor.execute(sql, val)
    mydb.commit()

def addWord(word):
    sql = "REPLACE INTO word (label) VALUES ('"+word+"')"
    mycursor.execute(sql)
    mydb.commit()

def addCity(city):
    sql = "REPLACE INTO city (city_name) VALUES ('"+city+"')"
    mycursor.execute(sql)
    mydb.commit()

def addKeywords(numero_tweet, city, wordList):
    addCity(city)
    for word in wordList:
        addWord(word)
        sql = "REPLACE INTO keyword (numero_tweet,city_name,label) VALUES (%s, %s, %s)"
        val = (numero_tweet, city, word)
        mycursor.execute(sql,val)
        mydb.commit()

def deleteQuestionMarksOnly():
    for i in range(100):
        str = ""
        for j in range(i):
            str += "?"
        sql = "DELETE FROM keyword WHERE label LIKE '"+str+"';"
        mycursor.execute(sql)
        sql = "DELETE FROM word WHERE label LIKE '"+str+"';"
        mycursor.execute(sql)
        mydb.commit()


def saveTweets(searched_word, number_max,only_located):
    #COORDS OF SOME FRENCH CITIES (ex : geocode="45.188529,5.724524,30km")
    #Grenoble : 45.188529,5.724524
    #Paris : 48.853,2.35
    for status in tweepy.Cursor(api.search, q=searched_word, tweet_mode='extended', geocode="45.188529,5.724524,30km").items(number_max):
        county="unknown"
        tweet = status._json
        tweet_id = tweet['id'] #the id of the tweet/retweet
        tweet_created_at = setDateTime(tweet['created_at']) # when the tweet posted
        tweet_text = tweet['full_text'] # content of the tweet
        tweet_user_id = tweet['user']['id'] # id of the user who posted the tweet
        tweet_user_name = tweet['user']['name'] # name of the user, e.g. "Wei Xu"
        tweet_user_screenname = tweet['user']['screen_name'] # name of the user account, e.g. "cocoweixu"
        #Only the real tweets are stored, not the retweets.
        if tweet_text[:2]!="RT":
            #IF THE USER SPECIFIED HIS LOCATION IN HIS TWEET, THIS LOCATION IS SAVED IN THE DATABASE AND THE TWEET IS DISPLAYED ON A MAP
            if tweet['place'] is not None and tweet['place']['bounding_box'] is not None and tweet['place']['bounding_box']['coordinates'] is not None:
                longitude, latitude = getLongAndLat(tweet['place']['bounding_box']['coordinates'][0])
                longitude, latitude = centrePolygone(longitude, latitude)
                try:
                    addr_infos = coords.get_address(latitude, longitude)
                    if "county" in addr_infos["address"]:
                        county = addr_infos["address"]["county"]
                        wordList = tokenizer.getKeyWords(tweet_text)
                        addKeywords(tweet_id, county, wordList)
                except:
                    pass
            else:
                longitude, latitude = (0,0)
            #only_located is set at True if the user wants to save only the located tweets (False if he wants to save all tweets)
            if not only_located or (only_located and longitude != 0):
                addTweet(tweet_created_at, tweet_text, tweet_user_id, tweet_user_name,
                         tweet_user_screenname, latitude, longitude, searched_word, county, tweet_id)


def displayAllTweets(city="",keyword=""):
    mycursor.execute("SELECT * FROM tweet WHERE nearest_city LIKE '%"+city+"%' AND searched_keyword LIKE '%"+keyword+"%'")
    myresult = mycursor.fetchall()
    map = coords.create_map()
    for line in myresult:
        #If there is a location (here we just try to check if there is a latitude):
        if line[6] != "0":
            addr_infos = coords.get_address(line[6], line[7])
            coords.add_marker(map, float(line[6]), float(line[7]), line[4], line[5], line[2],
                              str(line[1]), addr_infos["display_name"])
    map.save('map.html')


#saveTweets("", 1000000,True)
#displayAllTweets(city="Grenoble")
deleteQuestionMarksOnly()


# =============================================================================

# REQUETES SELECT
# =============================================================================
# mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM tweet")
# myresult = mycursor.fetchall()
# for line in myresult:
#     print(line)
# print(type(line))
# =============================================================================


# Recherche de mes derniers tweets
# =============================================================================
# tweets=api.user_timeline()
# for tweet in tweets:
#     print(tweet.text)
# =============================================================================

