###owl attack
        elif message.content.startswith('~owl'):
            try:
                await client.send_file(message.channel, getSubredditPictureSpecific('superbowl'))
            except Exception as e:
                await client.send_message(message.channel, ':shrug:')
        ###awwnime
        elif message.content.startswith('~aww'):
            try:
                await client.send_message(message.channel, getSubredditPictureSpecific('awwnime'))
            except Exception as e:
                await client.send_message(message.channel, ':shrug:')



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
                        print(redditApiResult)
                    else:
                        print('else ')
                        print(redditApiResult)
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
        return 'imgs/SFW/' + subreddit + '/' + fileName
    except Exception as e:
        print('Error in getSubredditPicture method:')
        print(e)
        return ':shrug:'