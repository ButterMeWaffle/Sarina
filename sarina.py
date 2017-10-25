import discord
import asyncio
import requests
import json
import random
import time
from io import BytesIO
import urllib.request
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
###all of my conditions for messages that trigger different functions
async def on_message(message):
    # l = dir(message)
    # print(l)
    #print(message.author)
    if not message.author.bot:
        if message.content.startswith('~test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        ###post pic from reddit, NSFW or SFW depending on below
        elif message.content.startswith('~r'):
            if message.channel.name == "nsfw" or message.channel.name == "gayboys":
                channelName = message.channel.name
                returnMessage = await getSubredditPictureNSFW(channelName,(message.content[3:]))
                await client.send_file(message.channel, returnMessage)
                os.remove(returnMessage)
            else:
                returnMessage = await getSubredditPicture(channelName,(message.content[3:]))
                await client.send_file(message.channel, returnMessage)
                os.remove(returnMessage)
        ###owl attack
        elif message.content.startswith('~owl'):
            try:
                returnMessage = getSubredditPictureSpecific('superbowl')
                print(returnMessage)
                await client.send_file(message.channel, returnMessage)
                os.remove(returnMessage)
            except Exception as e:
                print(e)
                await client.send_message(message.channel, ':shrug:')
        ###awwnime
        elif message.content.startswith('~aww'):
            try:
                await client.send_file(message.channel, getSubredditPictureSpecific('awwnime'))
            except Exception as e:
                await client.send_message(message.channel, ':shrug:')
        ###Tragedy indeed
        elif 'have you' in message.content or 'tragedy' in message.content or 'plagueis' in message.content or 'wise' in message.content or 'story' in message.content:
            await client.send_message(message.channel, 'Would you like to hear a story?')
            for line in TragedyIndeed :
                await client.send_message(message.channel, line)
                await asyncio.sleep(1)
        ###Some random funny commands
        elif 'test' in message.content:
            await client.send_message(message.channel, 'TEST REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
        elif 'fuck you' in message.content:
            await client.send_message(message.channel, 'Fuck you too')
        elif 'jack sparrow' in message.content:
            await client.send_message(message.channel, '***Captain*** Jack Sparrow')
        elif 'love you' in message.content or 'love sarina' in message.content or 'love this bot' in message.content:
            await client.send_message(message.channel, '***Captain*** Jack Sparrow')


        ###for explosion
        #for line in random.choice(listOfChants):
        #    await client.send_message(message.channel, line)
        #    await asyncio.sleep(0.5)

###Get stuff from reddit, SFW and NSFW
    ###SFW
def getSubredditPicture(subreddit="", nsfw=False):
    try:
        replyMessage = ':shrug:'
        if subreddit != '':
            client_auth = requests.auth.HTTPBasicAuth('BBJOcC2GtlKsYQ', 'WeFYWSVicZPiW6bT077bpWkNpH8')
            post_data = {'grant_type': 'client_credentials'}# post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
            requestHeaders = {'User-agent': 'linux:Sarina:v1 (by /u/thewafflekingg)'}
            redditAuthResult = json.loads(requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=requestHeaders).text)
            print('right before auth result')
            if redditAuthResult['access_token']:
                print('aftr auth result')
                requestHeaders2 = {'Authorization': 'bearer ' + redditAuthResult['access_token'], 'User-agent': 'linux:Sarina:v1 (by /u/thewafflekingg)'}
                maxReTries = 3
                gettingPicture = True
                
                while gettingPicture and maxReTries > 0:
                    redditApiResult = json.loads(requests.get('https://reddit.com/r/' + subreddit + '/random.json', headers=requestHeaders2).text)
                    print('apiresult')
                    print(maxReTries)
                    if isinstance(redditApiResult, dict):
                        randomInt = random.randint(0, len(redditApiResult['data']['children']) - 1)
                        redditApiResult = redditApiResult['data']['children'][randomInt]['data']
                        print("api result")
                    else:
                        print('else fired')
                        redditApiResult = redditApiResult[0]['data']['children'][0]['data']
                    if 'poop' not in redditApiResult['title'].lower() \
                        and redditApiResult['score'] > 10:
                        # and redditApiResult['domain'].lower() in imageDomains:
                            if nsfw is True and redditApiResult['over_18'] is True:
                                gettingPicture = False
                            elif nsfw is True:
                                gettingPicture = False
                    maxReTries = maxReTries - 1
                if not gettingPicture:
                    replyMessage = redditApiResult['url'].replace('amp;', '')
                    if replyMessage == ":shrug:":
                        return replyMessage
                    print(replyMessage)
                    fileName = replyMessage.split('/')[-1]
                    requestHeaders = {'User-agent': 'linux:Sarina:v1'}
                    imageResponse = requests.get(replyMessage, headers=requestHeaders, stream=True)
                    imageFile = open('imgs/SFW/' + fileName, 'wb')
                    imageFile.write(imageResponse.content)
                    imageFile.close()
        return 'imgs/SFW/' + fileName
    except Exception as e:
        print('Error in getSubredditPicture method:')
        print(e)
        return ':shrug:'

def getSubredditPictureSpecific(subreddit = '', nsfw=True):
    try:
        print(subreddit)
        replyMessage = ':shrug:'
        if subreddit != '':
            client_auth = requests.auth.HTTPBasicAuth('BBJOcC2GtlKsYQ', 'WeFYWSVicZPiW6bT077bpWkNpH8')
            post_data = {'grant_type': 'client_credentials'}# post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
            requestHeaders = {'User-agent': 'linux:Sarina:v1 (by /u/thewafflekingg)'}
            redditAuthResult = json.loads(requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=requestHeaders).text)
            
            if redditAuthResult['access_token']:
                requestHeaders2 = {'Authorization': 'bearer ' + redditAuthResult['access_token'], 'User-agent': 'linux:Sarina:v1 (by /u/thewafflekingg)'}
                maxReTries = 3
                gettingPicture = True
                while gettingPicture and maxReTries > 0:
                    redditApiResult = json.loads(requests.get('https://reddit.com/r/' + subreddit + '/random.json', headers=requestHeaders2).text)
                    if isinstance(redditApiResult, dict):
                        print('if isinstance')
                        randomInt = random.randint(0, len(redditApiResult['data']['children']) - 1)
                        redditApiResult = redditApiResult['data']['children'][randomInt]['data']
                    else:
                        print('else ')
                        redditApiResult = redditApiResult[0]['data']['children'][0]['data']
                    if 'poop' not in redditApiResult['title'].lower() \
                        and redditApiResult['score'] > 10:
                        # and redditApiResult['domain'].lower() in imageDomains:
                            if nsfw is True and redditApiResult['over_18'] is True:
                                gettingPicture = False
                            elif nsfw is True:
                                gettingPicture = False
                    maxReTries = maxReTries - 1
                if not gettingPicture:
                    replyMessage = redditApiResult['url'].replace('amp;', '')
                    print(replyMessage)
                    fileName = replyMessage.split('/')[-1]
                    requestHeaders = {'User-agent': 'linux:Sarina:v1'}
                    imageResponse = requests.get(replyMessage, headers=requestHeaders, stream=True)
                    imageFile = open('imgs/SFW/' + subreddit + '/' + fileName, 'wb')
                    imageFile.write(imageResponse.content)
                    imageFile.close()
                    print('imgs/' + fileName)
        return 'imgs/SFW/' + subreddit + '/' + fileName
    except Exception as e:
        print('Error in getSubredditPicture method:')
        print(e)
        return ':shrug:'


    ###NSFW

def getSubredditPictureNSFW( channelName, subreddit="",nsfw=True):
    try:
        replyMessage = ':shrug:'
        if subreddit != '':
            client_auth = requests.auth.HTTPBasicAuth('BBJOcC2GtlKsYQ', 'WeFYWSVicZPiW6bT077bpWkNpH8')
            post_data = {'grant_type': 'client_credentials'}# post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
            requestHeaders = {'User-agent': 'linux:Sarina:v1 (by /u/thewafflekingg)'}
            redditAuthResult = json.loads(requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=requestHeaders).text)
            
            if redditAuthResult['access_token']:
                requestHeaders2 = {'Authorization': 'bearer ' + redditAuthResult['access_token'], 'User-agent': 'linux:Sarina:v1 (by /u/thewafflekingg)'}
                maxReTries = 3
                gettingPicture = True
                while gettingPicture and maxReTries > 0:
                    redditApiResult = json.loads(requests.get('https://reddit.com/r/' + subreddit + '/random.json', headers=requestHeaders2).text)
                    if isinstance(redditApiResult, dict):
                        randomInt = random.randint(0, len(redditApiResult['data']['children']) - 1)
                        redditApiResult = redditApiResult['data']['children'][randomInt]['data']
                    else:
                        redditApiResult = redditApiResult[0]['data']['children'][0]['data']
                    if 'poop' not in redditApiResult['title'].lower() \
                        and redditApiResult['score'] > 10:
                        # and redditApiResult['domain'].lower() in imageDomains:
                            if nsfw is True and redditApiResult['over_18'] is True:
                                gettingPicture = False
                            elif nsfw is True:
                                gettingPicture = False
                    maxReTries = maxReTries - 1
                if not gettingPicture:
                    replyMessage = redditApiResult['url'].replace('amp;', '')
                    fileName = replyMessage.split('/')[-1]
                    print(replyMessage)
                    print(fileName)
                    requestHeaders = {'User-agent': 'linux:Sarina:v1'}
                    imageResponse = requests.get(replyMessage, headers=requestHeaders, stream=True)
                    imageFile = open('imgs/NSFW/' + fileName, 'wb')
                    imageFile.write(imageResponse.content)
                    imageFile.close()
        return 'imgs/NSFW/' + fileName    
    except Exception as e:
        print('Error in getSubredditPicture method:')
        print(e)
        return ':shrug:'

###end reddit posts

###funny random stuff

    ###Tragedy indeed

TragedyIndeed = [' **The Senate** - Did you ever hear the Tragedy of Darth Plagueis the Wise?', ' **Bitch Boy** - No.',' **The Senate** - I thought not.', ' **The Senate** - It’s not a story the Jedi would tell you.', ' **The Senate** - It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side, he could even keep the ones he cared about from dying.', ' **Bitch Boy** - He could actually...save people from death?', ' **The Senate** - The dark side of the Force is a pathway to many abilities some consider to be unnatural.', ' **Bitch Boy** - What happened to him?', ' **The Senate** - He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did.', ' **The Senate** - Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.', ' **Bitch Boy** - Is it possible to learn this power?', ' **The Senate** - Not from a Jedi.']


client.run('MzYzMjk4ODM0MjM2ODMzNzkz.DM-b8Q.Kjo_CUbsxR7QCG6goDyTGfTci0g')