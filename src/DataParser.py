from datetime import datetime
from datetime import timedelta
import mysql.connector


class dataParser():

    def __init__(self):
        """
        Initializes the dataParser by connecting to the database.
        ----------
        Parameters :
            No parameter.
        Returns :
            No return.
        """
        self.mydb = mysql.connector.connect(
                host = "localhost",
                port = "3306",
                user = "root",
                passwd = "root",
                database = "bgpstreamdb"
        )
        self.mycursor = self.mydb.cursor()

    def setDateTime(self,dateTweet):
        """
        Method that converts the tweet default date format to a date format compatible with MySQL databases (Python datetime)
        For example, "Mon Apr 01 17:09:19 +0000 2019" will be converted in "2019-04-01 18:09:00" (We add one hour to the time
        because we have UTC+2 in France)
        ----------
        Parameters :
            - dateTweet (str) : the tweet's publication date (and time)
        Returns :
            - d (datetime.datetime) : a datetime object
        """
        monthsDic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
                     "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        # We're getting the day,month,year,hour and minute from the tweet time to create a new datetime
        dateToString = dateTweet[8:10] + "/" + monthsDic[dateTweet[4:7]] + "/" + dateTweet[-2:]
        d = datetime.strptime(dateToString, "%d/%m/%y")
        h = dateTweet[dateTweet.find(':') - 2:dateTweet.find(':')]
        m = dateTweet[dateTweet.find(':') + 1:dateTweet.find(':') + 3]
        d = d.replace(hour=int(h), minute=int(m))
        # We add one hour to the time because we have UTC+1 in France
        d = d + timedelta(hours=2)
        return d

    def find_nth(self, string, substring, n):
        """
        Finds the index of the nth occurrence of a substring in a string.
        ----------
        Parameters :
            - string : the haystack string
            - substring : the needle string
            - n : the "n"th number (for example, if n = 5, the 5th occurrence of the substring will be found.)
        Returns :
            - the index of the substring
        """
        if (n == 1):
            return string.find(substring)
        else:
            return string.find(substring, self.find_nth(string, substring, n - 1) + 1)

    def addToDB(self, tweet):
        """
        Redirects to self.addToDB_OT or self.addToDB_HJ, depending on whether it's an Outage, a Hijack, or a Leak.
        ----------
        Parameters :
            - tweet : the tweet to add
        Returns :
            No Return
        """
        # Separates the text of the tweets to get only the first two letters of this text, which indicates the type of
        # alert.
        text_tweet = tweet["full_text"].split(",")
        if text_tweet[1] == "OT":
            self.addToDB_OT(tweet)
        if text_tweet[1] == "HJ":
            self.addToDB_HJ(tweet)
        # We didn't find any example of a Leak tweet on the BGPStream's twitter account, so this case isn't treated by
        # our program.
        if text_tweet[1] == "LK":
            pass


    def addToDB_OT(self, tweet):
        """
        Adds an Outage tweet to the database
        ----------
        Parameters :
            - tweet : the tweet to add
        Returns :
            No Return
        """
        text_tweet = tweet["full_text"]
        id_tweet = tweet["id_str"]
        date_tweet = self.setDateTime(tweet["created_at"])
        # Sometimes, the AS number is not specified (we only have information about the country) In this case, the 7th
        # character is a letter and not a number, so we chose to set the country name as the AS name.
        if(text_tweet[7].isalpha()):
            numAS_tweet = "Unknown"
            # AS Name is between the 3rd and the 4th comma
            ASName_tweet = text_tweet[self.find_nth(text_tweet, ",", 3) + 1:self.find_nth(text_tweet, ",", 4)]
            # the country code is between the 2nd and the 3rd comma
            code_country_tweet = text_tweet[self.find_nth(text_tweet, ",", 2) + 1:self.find_nth(text_tweet, ",", 3)]
        else:
            # the AS number is between the 2nd and the 3rd comma
            numAS_tweet = text_tweet[self.find_nth(text_tweet, ",", 2) + 1:self.find_nth(text_tweet, ",", 3)]
            # We analyze the part between the AS Number and the ",-," part of the text, which differs from time to time:
            AS_name_and_country = text_tweet[self.find_nth(text_tweet, ",", 3) + 1:text_tweet.find(",-,")]
            if(len(AS_name_and_country)>3 and AS_name_and_country[-3] == " " and AS_name_and_country[-2].isupper()):
                ASName_tweet = AS_name_and_country[:-4]
                code_country_tweet = AS_name_and_country[-2:]
            # In some cases, no country or AS Name is specified :
            else:
                ASName_tweet = "Unknown"
                code_country_tweet = "Unknown"
        nb_prefixes_tweet = text_tweet[text_tweet.find("Outage affected ")+16:text_tweet.find(" prefixes, ")]
        val = (id_tweet, date_tweet, numAS_tweet, ASName_tweet, code_country_tweet, nb_prefixes_tweet)
        sql = "INSERT INTO outage (id, date, numAS, nomAS, paysAS, nbPrefixe) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except:
            print("couldn't add the tweet number",id_tweet,"(probably already in the database)")


    def addToDB_HJ(self, tweet):
        """
        Adds a Hijack tweet to the database
        ----------
        Parameters :
            - tweet : the tweet to add
        Returns :
            No Return
        """
        text_tweet = tweet["full_text"]
        id_tweet = tweet["id_str"]
        date_tweet = self.setDateTime(tweet["created_at"])
        # prefix is between the 3rd space and the 3rd comma
        prefix = text_tweet[self.find_nth(text_tweet, " ", 3) + 1:self.find_nth(text_tweet, ",", 3)]
        # as_source is between the 2nd space and the 3rd space
        as_source = text_tweet[self.find_nth(text_tweet, " ", 2) + 3:self.find_nth(text_tweet, " ", 3)]
        # as_hijack is between the ",-, By" and the first space after ",-, By"
        as_hijack = text_tweet[text_tweet.find(",-,By ") + 8:text_tweet.find(" ", text_tweet.find(",-,By ") + 8)]
        val = (id_tweet, date_tweet, prefix, as_source, as_hijack)
        sql = "INSERT INTO hijack (id, date, prefixe, numASSource, numASHijack) VALUES (%s, %s, %s, %s, %s)"

        try:
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except:
            print("couldn't add the tweet number",id_tweet,"(probably already in the database)")

