import discord
import asyncio
import requests
import json
import random

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('~test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('~r'):
        await client.send_message(message.channel, getSubredditPicture(message.content[3:]))

def getSubredditPicture(subreddit="", nsfw=False):
    try:
        replyMessage = ':shrug:'
        if subreddit != '':
            client_auth = requests.auth.HTTPBasicAuth('BBJOcC2GtlKsYQ', 'WeFYWSVicZPiW6bT077bpWkNpH8')
            post_data = {'grant_type': 'client_credentials'}# post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
            requestHeaders = {'User-agent': 'linux:Sarin:v1 (by /u/thewafflekingg)'}
            redditAuthResult = json.loads(requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=requestHeaders).text)
            
            if redditAuthResult['access_token']:
                requestHeaders2 = {'Authorization': 'bearer ' + redditAuthResult['access_token'], 'User-agent': 'linux:ferretBot:v1 (by /u/digital_charon)'}
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
        return replyMessage
    except Exception as e:
        print('Error in getSubredditPicture method:')
        print(e)
        return ':shrug:'

client.run('MzYzMjk4ODM0MjM2ODMzNzkz.DM-b8Q.Kjo_CUbsxR7QCG6goDyTGfTci0g')