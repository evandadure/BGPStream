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