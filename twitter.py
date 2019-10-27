import tweepy
from datetime import datetime
import tokens

def getCalendar(username):

    auth = tweepy.OAuthHandler(tokens.con_key, tokens.con_sec)
    auth.set_access_token(tokens.sec_key, tokens.sec_sec)

    api = tweepy.API(auth)
    pastMonth = {}

    today = int(str(datetime.date(datetime.now()))[8:10])
    while today >= 1:
        pastMonth[(str(datetime.date(datetime.now()))[:8] + f"{today:02d}")] = []
        today -= 1

    allResults = False
    favorites = api.favorites(screen_name=username,count=199)
    while not allResults:
        if len(favorites) == 199:
            if str(favorites[198].created_at)[:7] != str(datetime.date(datetime.now()))[:7]:
                allResults = True
            else:
                maxid = favorites[-1].id
        else:
            allResults = True
        for fav in favorites:
            if str(datetime.date(datetime.now()))[:7] == str(fav.created_at)[:7]:
                pastMonth[str(fav.created_at)[:10]].append(str(fav.created_at)[11:])
        if allResults == False:
            favorites = api.favorites(screen_name=username,count=199,max_id=maxid)


    allResults = False
    tweets = api.user_timeline(screen_name=username,count=199,include_rts=True)
    while not allResults:
        if len(tweets) == 199:
            if str(tweets[198].created_at)[:7] != str(datetime.date(datetime.now()))[:7]:
                allResults = True
            else:
                maxid = tweets[-1].id
        else:
            allResults = True
        for tweet in tweets:
            if str(datetime.date(datetime.now()))[:7] == str(tweet.created_at)[:7]:
                pastMonth[str(tweet.created_at)[:10]].append(str(tweet.created_at)[11:])
        if allResults == False:
            tweets = api.user_timeline(screen_name=username,count=199,max_id=maxid,include_rts=True)

    return pastMonth

demo = getCalendar('jalfrazi_')

for k,v in demo.items():
    print(k + ' - ' + ', '.join(v))