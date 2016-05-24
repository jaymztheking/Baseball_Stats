# Baseball Stats

##Overview
This project is a collection of Python classes and corresponding PostgreSQL components developed in order to scrape data off baseball statistic websites and load into an OLAP-ish database structure

##Pre-Requisites
* Python 2.7.10
* PostgreSQL
* psycopg2

##Notes
* 2001-08-04 KCA at MIN has a game time of 6:06Ac, i guess

##To - Do
* Run code for 1993 - 2001ish
* Get Current Year Files
* Run BR script
* Write code to scrape day-of lineups and salaries (MLB.com? DK?)

##Pitch Result Tests
* Start Situation is not 30
* End Situation for Home Run ends in 0
* Start Sit generally doesn't equal end sit when no RBIs
* Start Sit =21 and End Sit =21 on double plays
* Game 2077 is weird in Top 8
