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
* Run code for 1993 - 2011
* Create table for per plate appearance stats
* Create play by play scraping for current year
* Write code to scrape day-of lineups and salaries

##Pitch Result Tests
* Start Situation is not 30
* End Situation for Home Run ends in 0
* Start Sit generally doesn't equal end sit when no RBIs
* Start Sit =21 and End Sit =21 on double plays
