# BGPStream

The aim of this school project was to collect and parse the different tweets of the Twitter account @bgpstream. "BGP Stream is a free resource for receiving alerts about hijacks, leaks, and outages in the Border Gateway Protocol." (source : https://bgpstream.com)

# How to use our program

The program is quite simple : it allows the user to use either the Stream API or the Search API of Tweepy, in order to get respectively the incoming and the previous tweets of the BGPStream account.
We created a Main.py file to gather these features, you just have to give it a quick look and run it !

# The database

The tweets can be stored in a MySQL database. The SQL code to create the tables can be found in data/tweetDB.sql. The database only contains two tables : Outage and Hijack, storing the most relevant information for each type of alert.

# About us

The two students behind this project, Evan Dadure and Maxence Personnaz (https://github.com/MaxencePRSZ), are studying in the Polytech Annecy-Chambéry engineering school, in the IT and Data Usage program.
