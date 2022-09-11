# Discord-Scraper
Take Messages from user specified discord channels and store the messages in an SQL server.

## Usage
The program takes inputted channel IDs from a `Channel_ids.txt`. Each time a new channel ID is placed in the `Channel_ids.txt`, the last 5 messages from that channel are requested. For channels already in the database on messages after the last save are recieved.

## Prerequisites
The architecture of the MySQL database is as follows.
![sqldatabase](sqldesign.JPG)
## Requirements
Two library installations are required for this project. 
The first being the `requests` library and the second being `mysql.connector`.
```shell
pip install requests
pip install mysql-connector-python
```

## Declarations
```python
header = {'authorization' : '...'}
```
This is a token for the Discord user account. This can be taken from the Discord Developer Portal.
```python
database = '...'
pw = '...'
```
These declare the name and password of the local database.
