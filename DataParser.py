import re
import mysql.connector


class dataParser():

    # =============================================================================
    #     host="tp-epu.univ-savoie.fr",
    #     port="3308",
    #     user="personma",
    #     passwd="rca8v7gd",
    #     database="personma"
    # =============================================================================

    # =============================================================================
    #     host = "localhost",
    #     port = "3306",
    #     user = "root",
    #     passwd = "root",
    #     database = "bgpstreamdb"
    # =============================================================================

    def __init__(self):

        self.mydb = mysql.connector.connect(
            host="tp-epu.univ-savoie.fr",
            port="3308",
            user="personma",
            passwd="rca8v7gd",
            database="personma"
        )


    def find_nth(self, string, substring, n):
        if (n == 1):
            return string.find(substring)
        else:
            return string.find(substring, self.find_nth(string, substring, n - 1) + 1)

    def addToDB(self, tweet):
        text_tweet = tweet["full_text"].split(",")
        if text_tweet[1] == "OT":
            self.addToDB_OT(tweet)
        if text_tweet[1] == "HJ":
            self.addToDB_HJ(tweet)
        if text_tweet[1] == "LK":
            pass


# =============================================================================
# list index out of range
# BGP,OT,268434,--No Registry Entry--,-,Outage affected 24 prefixes, https://t.co/SyjUaDYStb
# =============================================================================


    def addToDB_OT(self, tweet):
        mycursor = self.mydb.cursor()
        text_tweet = tweet["full_text"].split(",")
        text = text_tweet[2]
        pattern = '\d+'
        print(tweet["full_text"])
        if re.match(pattern, text):
            text_tweet = self.standardize(text_tweet, 8, 3)
            nbPref = re.findall(pattern, text_tweet[6])[0]
            val = (tweet["id_str"], text, text_tweet[3], text_tweet[4], nbPref)
            sql = "INSERT INTO Outage (id, numAS, nomAS, paysAS, nbPrefixe) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(sql, val)
        else:
            nbPref = re.findall(pattern, text_tweet[5])[0]
            val = (tweet["id_str"], text_tweet[3], text, nbPref)
            sql = "INSERT INTO Outage (id, numAS, nomAS, paysAS, nbPrefixe) VALUES (%s, \'\', %s, %s, %s)"
            mycursor.execute(sql, val)
            
    def standardize(self, text_tweet, length, first_occur):
        while len(text_tweet) > length:
            text_tweet[first_occur] += "," + text_tweet[first_occur+1]
            text_tweet.pop(first_occur+1)
        return text_tweet

    def standardize(self, text_tweet, length, first_occur):
        while len(text_tweet) > length:
            text_tweet[first_occur] += "," + text_tweet[first_occur + 1]
            text_tweet.pop(first_occur + 1)
        return text_tweet

    def addToDB_HJ(self, tweet):
        mycursor = self.mydb.cursor()
        text_tweet = tweet["full_text"]
        id_tweet = tweet["id_str"]
        as_source = text_tweet[text_tweet.find("prefix") + 9:self.find_nth(text_tweet, " ", 3)]
        prefixe = text_tweet[self.find_nth(text_tweet, " ", 3) + 1:self.find_nth(text_tweet, ",", 3)]
        as_hijack = text_tweet[text_tweet.find(",-,By ") + 8:text_tweet.find(" ", text_tweet.find(",-,By ") + 8)]

        val = (id_tweet, prefixe, as_source, as_hijack)
        sql = "INSERT INTO Hijack (id, prefixe, numASSource, numASHijack) VALUES (%s, %s, %s, %s)"
        # sql = "INSERT INTO hijack (id, prefixe, numASSource, numASHijack) VALUES ('"+id_tweet+"','"+prefixe+"','"+as_source+"','"+as_hijack+"')"
        mycursor.execute(sql, val)

        # mycursor = self.mydb.cursor()
        # mycursor.execute("SELECT * FROM hijack")
        # myresult = mycursor.fetchall()
        # for line in myresult:
        #     print(line)

#
# CREATE TABLE Outage(
# id varchar(255),
# numAS varchar(255),
# nomAS varchar(255),
# paysAS varchar(255),
# nbPrefixe varchar(255)
# );
# CREATE TABLE Hijack(
# id varchar(255),
# prefixe varchar(255),
# numASSource varchar(255),
# numASHijack varchar(255)
# );
# CREATE TABLE Leak(
# id varchar(255),
# numAS varchar(255),
# nomAS varchar(255),
# paysAS varchar(255),
# source varchar(255),
# destination varchar(255)
# );