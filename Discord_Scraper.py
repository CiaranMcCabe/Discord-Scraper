import requests
import mysql.connector
from mysql.connector import Error
import os


header = { 'authorization' : '...'}
database = '...'
pw = '...'

#------------------API INTERACTIONS-----------------------
def get_channelids(connection):
    if os.stat("Channel_ids.txt").st_size != 0:
        filename = open("Channel_ids.txt","r+")
        channel_ids = filename.readlines()
        filename.truncate(0)
        filename.close()
        get_guildinfo(channel_ids, connection)
    mycursor = connection.cursor()
    mycursor.execute("SELECT ChannelID, LastmessID FROM channels")
    channels = mycursor.fetchall()
    return channels
        
def get_guildinfo(channel_ids, connection):
    for id in channel_ids:
        get_channel = requests.get(f'https://discordapp.com/api/v9/channels/{id}', headers=header)
        channel_info = get_channel.json()
        guild_id = channel_info['guild_id']
        get_guild = requests.get(f'https://discordapp.com/api/v9/guilds/{guild_id}', headers=header)
        guild_info = get_guild.json()
        #print(guild_info['id'], guild_info['name'])
        guild_query(connection, guild_info['id'], guild_info['name'])
        #print(channel_info['id'], channel_info['name'])
        channel_query(connection, channel_info['id'], channel_info['name'], guild_info['id'])
    return 
    
def channel_messages(connection, channels):
    for channel in channels:
        if channel[1] == None:
            getmessages = requests.get(f'https://discordapp.com/api/v9/channels/{channel[0]}/messages?limit=5', headers=header)
            messages = getmessages.json()
        else:
            getmessages = requests.get(f'https://discordapp.com/api/v9/channels/{channel[0]}/messages?after={channel[1]}', headers=header)
            messages = getmessages.json()
        for message in messages:
            message_query(connection, message['id'], message['author']['username'], message['content'], message['timestamp'], message['channel_id'])
            lastmess_query(connection, message['channel_id'], message['id'])
        



#----------------SQL SERVER INTERACTIONS/QUERIES----------------------

def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database = db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def guild_query(connection, id, name):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO guilds (GuildID, GuildName) VALUES (%s,%s)", (id, name))
        connection.commit()
        print('Guild Query Done')
    except Error as err:
        print(f"Error: '{err}'")

def channel_query(connection, channel_id, name, guild_id):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO channels (ChannelID, ChannelName, GuildID) VALUES (%s,%s,%s)", (channel_id, name, guild_id))
        connection.commit()
        print('Channel Query Done')
    except Error as err:
        print(f"Error: '{err}'")

def message_query(connection, message_id, author, content, timestamp, channel_id):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO messages (MessageID, Author, Content, Timestmp, ChannelID) VALUES (%s,%s,%s,%s,%s)", (message_id, author, content, timestamp, channel_id))
        connection.commit()
        print('Message Query Done')
    except Error as err:
        print(f"Error: '{err}'")
    
def lastmess_query(connection, channelid, lastmessid):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE channels SET LastMessID=(%s) WHERE ChannelID=(%s)", (lastmessid, channelid))
        connection.commit()
        print('Last Message Query Done')
    except Error as err:
        print(f"Error: '{err}'")    


#----------------------------MAIN--------------------------------
def main():
    connection = create_server_connection("localhost", "root", pw, database)
    channels = get_channelids(connection)
    channel_messages(connection, channels)
    

if __name__ == "__main__":
    main()
