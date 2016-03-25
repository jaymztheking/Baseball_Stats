# Baseball Stats

##Overview
This project is a collection of Python classes and corresponding PostgreSQL components developed in order to scrape data off baseball statistic websites and load into an OLAP-ish database structure

##Pre-Requisites
* Python 2.7.10
* PostgreSQL
* psycopg2

##Notes
* Pitcher hot streak flagging should be implemented
* Use retrosheet for play-by-play

##To - Do
* Create views for data framing, specifically for points and driver variables (wOBA, BABIP, ISO, HR/FB)
* Create view for finding missing games
* Complete play result code
* Write import code for pitch data
