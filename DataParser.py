import mysql.connector

class dataParser():
    
    def __init__(self):
        self.mydb= mysql.connector.connect(
                       host="tp-epu.univ-savoie.fr",
                       port="3308",
                       user="personma",
                       passwd="rca8v7gd",
                       database="personma"
                   )
    
    def addToDB(self, tweet):
        mycursor = mydb.cursor()
        text_tweet = tweet["text"].split(",")
        if text_tweet[1] == "OT":
            return 
        if text_tweet[1] == "HJ":
            return
        if text_tweet[1] == "LK":
            return
        sql = "INSERT INTO Tweet (created_at, text, user_ID, user_name, screen_name, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = ()
        mycursor.execute(sql, val)
        
        
        

# =============================================================================
#               SQL POUR CRÉER LES TABLES
        
# =============================================================================
#DROP TABLE IF EXISTS Hijack;
#
#CREATE TABLE Hijack(
# numAS varchar(255),
# nomAS varchar(255),
# paysAS varchar(255),
# prefixe varchar(255),
# adresseSource varchar(255),
# adresseDesti varchar(255)
#)
#
#CREATE TABLE Outage(
# numAS varchar(255),
# nomAS varchar(255),
# paysAS varchar(255),
# nbPrefixe varchar(255)
#)
#
#CREATE TABLE Leak(
# numAS varchar(255),
# nomAS varchar(255),
# paysAS varchar(255),
# source varchar(255),
# destination varchar(255)
#)
#)