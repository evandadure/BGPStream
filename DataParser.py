import mysql.connector


mydb = mysql.connector.connect(
  host="tp-epu.univ-savoie.fr",
  port="3308",
  user="personma",
  passwd="rca8v7gd",
  database="personma"
)
mycursor = mydb.cursor()

sql = "INSERT INTO Tweet (created_at, text, user_ID, user_name, screen_name, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = ()
mycursor.execute(sql, val)

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