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
    
    
    def __init__(self):
        self.mydb= mysql.connector.connect(
                       host="tp-epu.univ-savoie.fr",
                       port="3308",
                       user="personma",
                       passwd="rca8v7gd",
                       database="personma"
                   )
    
    def addToDB(self, tweet):
        text_tweet = tweet["text"].split(",")
        if text_tweet[1] == "OT":
            self.addToDB_OT(tweet)
        if text_tweet[1] == "HJ":
            return
        if text_tweet[1] == "LK":
            return

        
    def addToDB_OT(self, tweet):
        mycursor = self.mydb.cursor()
        text_tweet = tweet["text"].split(",")
        text = text_tweet[2]
        pattern = '\d+'
        print(text_tweet)
        if re.match(pattern, text):
            nbPref = re.findall(pattern, text_tweet[6])[0]
            val = (tweet["id_str"], text, text_tweet[3], text_tweet[4], nbPref)
            sql = "INSERT INTO Outage (id, numAS, nomAS, paysAS, nbPrefixe) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(sql, val)
        else:
            nbPref = re.findall(pattern, text_tweet[5])[0]
            val = (tweet["id_str"],  text_tweet[3], text, nbPref)
            sql = "INSERT INTO Outage (id, numAS, nomAS, paysAS, nbPrefixe) VALUES (%s, \'\', %s, %s, %s)"
            mycursor.execute(sql, val)
            
    def standardize(self, text_tweet, length, first_occur):
        while len(text_tweet) > length:
            text_tweet[3] += text_tweet[4]
            


# =============================================================================
#               SQL POUR CRÉER LES TABLES
# =============================================================================
#DROP TABLE IF EXISTS Hijack;
#DROP TABLE IF EXISTS Outage;
#DROP TABLE IF EXISTS Leak;
#
#CREATE TABLE Outage(
# id varchar(255),
# numAS varchar(255),
# nomAS varchar(255),
# paysAS varchar(255),
# nbPrefixe varchar(255)
#);
#CREATE TABLE Hijack(
# id varchar(255),
# numAS varchar(255),
# nomAS varchar(255),
# paysAS varchar(255),
# prefixe varchar(255),
# adresseSource varchar(255),
# adresseDesti varchar(255)
#);
#
#
#CREATE TABLE Leak(
# id varchar(255),
# numAS varchar(255),
# nomAS varchar(255),
# paysAS varchar(255),
# source varchar(255),
# destination varchar(255)
#);