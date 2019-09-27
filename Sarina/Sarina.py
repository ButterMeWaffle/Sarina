####
## Import libraries
####
import discord
from random import uniform
import asyncio
import requests
import json
import random
import time
from io import BytesIO
import urllib.request
import os
from urllib.parse import urlparse
from os.path import splitext

####
## Discord
####

token = "DiscordToken"

authToken = "authToken"
appId = "-appID"

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    checkAndMakeFolders()

# check and add urls as needed to save imgs
def checkAndMakeFolders():
    for url in pathList:
        if not os.path.exists(url):
            os.makedirs(url)
# check file extensions 
def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    print(ext)
    return ext  # or ext[1:] if you don't want the leading '.'

@client.event
###all of my conditions for messages that trigger different functions
async def on_message(message):
    # l = dir(message)
    # print(l)
    #print(message.author)
    if not message.author.bot:
        ### send all request to the request channel
        if message.content.startswith('~request'):
            await message.channel.trigger_typing()
            await client.send_message(discord.Object(id='488822810647724032'), message.content[8:] + " -User- " + message.author.name)
            await message.channel.send('Request sent, be patient!')
        ### still in the works
        elif message.content.startswith('~commands'):
            await message.channel.trigger_typing()
            print(message.channel.name)
            if message.guild.name == "SpaceBros":
                print(message.guild.name)
                await message.channel.send(cmdList)
            else:
                await message.channel.send(cmdList_Twitch)
        ###post pic from reddit, NSFW or SFW depending on below
        elif message.content.startswith('~r'):
            await message.channel.trigger_typing()
            if message.channel.name == "nsfw" or message.channel.name == "gayboys":
                
                returnMessage = getSubredditPictureNSFW(message.content[3:])
                print(returnMessage)
                if not returnMessage.startswith('imgs'):
                    await message.channel.send(file=discord.File(returnMessage))
                else: 
                    await message.channel.send(file=discord.File(returnMessage))
                    # remove pics
                    os.remove(returnMessage)
            else:
                returnMessage = getSubredditPicture(message.content[3:])
                if not returnMessage.startswith('imgs'):
                    await message.channel.send(file=discord.File(returnMessage))
                else: 
                    await message.channel.send(file=discord.File(returnMessage))
                    # remove pics
                    os.remove(returnMessage)
        ###owl attack
        elif message.content.startswith('~owl'):
            await message.channel.trigger_typing()
            try:
                returnMessage = getSubredditPictureSpecific('superbowl')
                print(returnMessage)
                if not returnMessage.startswith('imgs'):
                    await message.channel.send(file=discord.File(returnMessage))
                else: 
                    await message.channel.send(file=discord.File(returnMessage))
                    # remove pics
                    os.remove(returnMessage)
            except Exception as e:
                print(e)
                await message.channel.send(':shrug:')
        ###awwnime
        elif message.content.startswith('~aww'):
            await message.channel.trigger_typing()
            try:
                returnMessage = getSubredditPictureSpecific('awwnime')
                if not returnMessage.startswith('imgs'):
                    await message.channel.send(file=discord.File(returnMessage))
                else: 
                    await message.channel.send(file=discord.File(returnMessage))
                    # dont remove aww pics
                    # os.remove(returnMessage)
            except Exception as e:
                await message.channel.send(':shrug:')
        ###EarthPorn
        elif message.content.startswith('~ep'):
            await message.channel.trigger_typing()
            try:
                returnMessage = getSubredditPictureSpecific('earthporn')
                if not returnMessage.startswith('imgs'):
                    await message.channel.send(file=discord.File(returnMessage))
                else: 
                    await message.channel.send(file=discord.File(returnMessage))
                    # dont remove ep pics
                    # os.remove(returnMessage)
            except Exception as e:
                print(e)
                await message.channel.send(':shrug:')
        ###birb
        elif message.content.startswith('~birb'):
            await message.channel.trigger_typing()
            try:
                returnMessage = getSubredditPictureSpecific('birb')
                if not returnMessage.startswith('imgs'):
                    await message.channel.send(file=discord.File(returnMessage))
                else: 
                    await message.channel.send(file=discord.File(returnMessage))
                    # remove pics
                    os.remove(returnMessage)
            except Exception as e:
                await message.channel.send(':shrug:')
        ###xmas / temp?
        elif message.content.startswith('~xmas'):
            await message.channel.trigger_typing()
            try:
                returnMessage = getSubredditPictureSpecific('christmas')
                if not returnMessage.startswith('imgs'):
                    await message.channel.send(file=discord.File(returnMessage))
                else: 
                    await message.channel.send(file=discord.File(returnMessage))
                    # remove pics
                    os.remove(returnMessage)
            except Exception as e:
                await message.channel.send(':shrug:')
        ###NSFW
        elif message.content.startswith('~nsfw'):
            await message.channel.trigger_typing()
            if message.channel.name == "nsfw":
                try:
                    subreddit = nsfwSubs[random.randint(0, len(nsfwSubs))]
                    print(subreddit)
                    returnMessage = getSubredditPictureNSFW(subreddit)
                    if not returnMessage.startswith('imgs'):
                        await message.channel.send(file=discord.File(returnMessage))
                    else: 
                        await message.channel.send(file=discord.File(returnMessage))
                        # remove pics
                        os.remove(returnMessage)
                except Exception as e:
                    await message.channel.send(':shrug:')
        elif message.content.startswith('~lewd'):
           
            await message.channel.trigger_typing()
            if message.channel.name == "nsfw":
                try:
                    subreddit = lewd[random.randint(0, len(lewd))]
                    print(subreddit)
                    returnMessage = getSubredditPictureLewd(subreddit)
                    if not returnMessage.startswith('imgs'):
                        await message.channel.send(file=discord.File(returnMessage))
                    else: 
                        await message.channel.send(file=discord.File(returnMessage))
                        # remove pics
                        os.remove(returnMessage)
                except Exception as e:
                    await message.channel.send(':shrug:')
        ###Tragedy indeed
        #elif 'have you' in message.content or 'tragedy' in message.content or 'plagueis' in message.content or 'wise' in message.content or 'story' in message.content:
        #    await message.channel.trigger_typing()
        #    await message.channel.send('Would you like to hear a story?')
        #    for line in TragedyIndeed :
        #        await message.channel.trigger_typing()
        #        await message.channel.send(line)
        #        await asyncio.sleep(1)
        ###Help command, list out all usable commands besides the random funny below
        elif message.content.startswith('~help'):
            await message.channel.trigger_typing()
            await message.channel.send('--SFW commands-- \n    ~r subredditname  \n    ~owl (superbowl)  \n    ~birb (birb)  \n    ~aww (awwnime)  \n    ~ep  (earthporn)  \n    ~xmas  (christmaslights)\n\n')
            await message.channel.send('--NSFW commands-- \n    ~r subredditname  \n    ~lewd (variety/2D)  \n    ~nsfw (variety)')
        ###Some random funny commands
        #elif 'test' in message.content:
        #    await message.channel.trigger_typing()
        #    await message.channel.send('TEST REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
        elif 'fuck you' in message.content:
            await message.channel.trigger_typing()
            await message.channel.send('imgs/smug.jpg')
        elif 'jack sparrow' in message.content:
            await message.channel.trigger_typing()
            await message.channel.send('***Captain*** Jack Sparrow')
        elif 'love you' in message.content or 'love BotName' in message.content or 'love this bot' in message.content:
            await message.channel.trigger_typing()
            await message.channel.send('Love you too')
        elif 'bad bot' in message.content or 'bad BotName' in message.content:
            await message.channel.trigger_typing()
            await message.channel.send("I'm sorry D:")
        elif 'good bot' in message.content or 'good BotName' in message.content:
            await message.channel.trigger_typing()
            await message.channel.send("Thanks :) <3")
        elif 'thanks bot' in message.content or 'thanks BotName' in message.content or 'thanks BotName!' in message.content:
            await message.channel.trigger_typing()
            await message.channel.send("You're welcome :)")


        ###for explosion
        #for line in random.choice(listOfChants):
        #    await message.channel.send(line)
        #    await asyncio.sleep(0.5)

###Get stuff from reddit, SFW and NSFW
    ###SFW
def getSubredditPicture(subreddit="", nsfw=False):
    try:
        print(subreddit)
        replyMessage = ':shrug:'
        if subreddit != '':
            client_auth = requests.auth.HTTPBasicAuth(appId, authToken)
            post_data = {'grant_type': 'client_credentials'}# post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
            requestHeaders = {'User-agent': 'linux:BotName:v1 (by /u/RedditUser)'}
            redditAuthResult = json.loads(requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=requestHeaders).text)
            if redditAuthResult['access_token']:
                requestHeaders2 = {'Authorization': 'bearer ' + redditAuthResult['access_token'], 'User-agent': 'linux:BotName:v1 (by /u/RedditUser)'}
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
                            if nsfw is False and redditApiResult['over_18'] is False:
                                gettingPicture = False
                            elif nsfw is True:
                                gettingPicture = False
                    maxReTries = maxReTries - 1
                if not gettingPicture:
                    replyMessage = redditApiResult['url'].replace('amp;', '')
                    imageResponse = redditApiResult['url'].replace('amp;', '')
                    print(replyMessage)
                    if get_ext(replyMessage) == '' or get_ext(replyMessage) == '.gifv' or get_ext(replyMessage) == '.mp4' or get_ext(replyMessage) == '.html':
                        return replyMessage
                    else:
                        replyMessage = replyMessage.split('/')[-1]
                        requestHeaders = {'User-agent': 'linux:BotName:v1'}
                        imageResponse = requests.get(imageResponse, headers=requestHeaders, stream=True)
                        imageFile = open('imgs/SFW/' + replyMessage, 'wb')
                        imageFile.write(imageResponse.content)
                        imageFile.close()
                        replyMessage = 'imgs/SFW/' + replyMessage
        return replyMessage
    except Exception as e:
        print('Error in getSubredditPicture method:')
        print(e)
        return ':shrug:'

def getSubredditPictureSpecific(subreddit = '', nsfw=True):
    try:
        print(subreddit)
        replyMessage = ':shrug:'
        if subreddit != '':
            client_auth = requests.auth.HTTPBasicAuth(appId, authToken)
            post_data = {'grant_type': 'client_credentials'}# post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
            requestHeaders = {'User-agent': 'linux:BotName:v1 (by /u/RedditUser)'}
            redditAuthResult = json.loads(requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=requestHeaders).text)
            if redditAuthResult['access_token']:
                requestHeaders2 = {'Authorization': 'bearer ' + redditAuthResult['access_token'], 'User-agent': 'linux:BotName:v1 (by /u/RedditUser)'}
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
                            if nsfw is False and redditApiResult['over_18'] is False:
                                gettingPicture = False
                            elif nsfw is True:
                                gettingPicture = False
                    maxReTries = maxReTries - 1
                if not gettingPicture:
                    replyMessage = redditApiResult['url'].replace('amp;', '')
                    imageResponse = redditApiResult['url'].replace('amp;', '')
                    if get_ext(replyMessage) == '' or get_ext(replyMessage) == '.gifv' or get_ext(replyMessage) == '.mp4' or get_ext(replyMessage) == '.html':
                        return replyMessage
                    else:
                        replyMessage = replyMessage.split('/')[-1]
                        requestHeaders = {'User-agent': 'linux:BotName:v1'}
                        imageResponse = requests.get(imageResponse, headers=requestHeaders, stream=True)
                        imageFile = open('imgs/SFW/' + subreddit + '/' + replyMessage, 'wb')
                        imageFile.write(imageResponse.content)
                        imageFile.close()
                        replyMessage = 'imgs/SFW/' + subreddit + '/' + replyMessage
        return replyMessage
    except Exception as e:
        print('Error in getSubredditPictureSpecific method:')
        print(e)
        return ':shrug:'


    ###NSFW

def getSubredditPictureNSFW(subreddit="",nsfw=True):
    try:
        replyMessage = ':shrug:'
        if subreddit != '':
            client_auth = requests.auth.HTTPBasicAuth(appId, authToken)
            post_data = {'grant_type': 'client_credentials'}# post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
            requestHeaders = {'User-agent': 'linux:BotName:v1 (by /u/RedditUser)'}
            redditAuthResult = json.loads(requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=requestHeaders).text)
            
            if redditAuthResult['access_token']:
                requestHeaders2 = {'Authorization': 'bearer ' + redditAuthResult['access_token'], 'User-agent': 'linux:BotName:v1 (by /u/RedditUser)'}
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
                    imageResponse = redditApiResult['url'].replace('amp;', '')
                    print(replyMessage)
                    if get_ext(replyMessage) == '' or get_ext(replyMessage) == '.gifv' or get_ext(replyMessage) == '.mp4' or get_ext(replyMessage) == '.html':
                        return replyMessage
                    else:
                        replyMessage = replyMessage.split('/')[-1]
                        requestHeaders = {'User-agent': 'linux:BotName:v1'}
                        imageResponse = requests.get(imageResponse, headers=requestHeaders, stream=True)
                        imageFile = open('imgs/NSFW/' + replyMessage, 'wb')
                        imageFile.write(imageResponse.content)
                        imageFile.close()
                        replyMessage = 'imgs/NSFW/' + replyMessage
        return replyMessage   
    except Exception as e:
        print('Error in getSubredditPictureNSFW method:')
        print(e)
        return ':shrug:'
   ###for soem nsfw anime subs, saves img
def getSubredditPictureLewd(subreddit = '', nsfw=True):
    try:
        print(subreddit)
        replyMessage = ':shrug:'
        if subreddit != '':
            client_auth = requests.auth.HTTPBasicAuth(appId, authToken)
            post_data = {'grant_type': 'client_credentials'}# post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
            requestHeaders = {'User-agent': 'linux:BotName:v1 (by /u/RedditUser)'}
            redditAuthResult = json.loads(requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=requestHeaders).text)
            if redditAuthResult['access_token']:
                requestHeaders2 = {'Authorization': 'bearer ' + redditAuthResult['access_token'], 'User-agent': 'linux:BotName:v1 (by /u/RedditUser)'}
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
                    imageResponse = redditApiResult['url'].replace('amp;', '')
                    if get_ext(replyMessage) == '' or get_ext(replyMessage) == '.gifv' or get_ext(replyMessage) == '.mp4' or get_ext(replyMessage) == '.html':
                        return replyMessage
                    else:
                        replyMessage = replyMessage.split('/')[-1]
                        requestHeaders = {'User-agent': 'linux:BotName:v1'}
                        imageResponse = requests.get(imageResponse, headers=requestHeaders, stream=True)
                        imageFile = open('imgs/NSFW/lewd/' + replyMessage, 'wb')
                        imageFile.write(imageResponse.content)
                        imageFile.close()
                        replyMessage = 'imgs/NSFW/lewd/' + replyMessage
        return replyMessage
    except Exception as e:
        print('Error in getSubredditPictureLewd method:')
        print(e)
        return ':shrug:'

###end reddit posts


###Tragedy indeed
TragedyIndeed = [' **The Senate** - Did you ever hear the Tragedy of Darth Plagueis the Wise?', ' **Bitch Boy** - No.',' **The Senate** - I thought not.', ' **The Senate** - It’s not a story the Jedi would tell you.', ' **The Senate** - It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side, he could even keep the ones he cared about from dying.', ' **Bitch Boy** - He could actually...save people from death?', ' **The Senate** - The dark side of the Force is a pathway to many abilities some consider to be unnatural.', ' **Bitch Boy** - What happened to him?', ' **The Senate** - He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did.', ' **The Senate** - Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.', ' **Bitch Boy** - Is it possible to learn this power?', ' **The Senate** - Not from a Jedi.']

# list of paths to create at start of program
pathList = ['imgs/', 'imgs/NSFW', 'imgs/NSFW/lewd', 'imgs/SFW', 'imgs/SFW/earthporn', 'imgs/SFW/superbowl', 'imgs/SFW/awwnime', 'imgs/SFW/christmas', 'imgs/SFW/birb']

# list of subreddits to choose from for random commands
nsfwSubs = ['nsfw', 'realgirls', 'nsfw_gif', 'Blowjob', 'Blowjobs', 'blowjobsandwich', 'boobies', 'collegesluts', 'DillionHarper', 'dirtysmall', 'dreamjobs', 'festivalsluts', 'funsized', 'girlskissing', 'porninfifteenseconds','RemyLaCroix', 'RileyReid', 'xsome', 'legalteens']
lewd = ['ecchi', 'hentai', 'yuri', 'nekomimi', 'efhentai', 'shoujoai', 'thelostwoods', 'cumhentai']

cmdList = 'Both - ~r subredditName SFW - ~owl, ~birb, ~ep, ~aww, ~xmas NSFW - ~NSFW, ~lewd. For reqests simply type in ~request "put your request here."' 

cmdList_Twitch = 'Both - ~r subredditName SFW - ~owl, ~birb, ~ep, ~aww, ~xmas... For reqests simply type in ~request "put your request here."' 

# now lets run it
client.run(token)

####
## Twitch
####