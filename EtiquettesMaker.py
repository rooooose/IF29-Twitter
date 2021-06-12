from service import rethinkDBservice

users = rethinkDBservice.getUsersCursors()

ageMax = 200
agressiviteMax = 10
visibilityMax = 0.3
tweetsPerDayMax = 15
ratioFollowersFriendsMax = 0.1
avgHashtagMax = 0.3
avgUrlMax = 1.5

nbSuspectTweets = 2055
rang = 0
for user in users:
    rang+=1
    print(rang)
#    if(user["verified"]):
#        rethinkDBservice.updateUser(user["id"], {"suspect": -1})
    if (user.get("suspect") == None):
        attributsSus = 0
        if user["accountAge(days)"] < 200:
            attributsSus+=1
        if user["agressivite"] > agressiviteMax:
            attributsSus+=1
        if user["visibility"] > visibilityMax:
            attributsSus+=1
        if user["tweet_per_day"] > tweetsPerDayMax:
            attributsSus+=1
        if user["rationFollowersFriends"] < ratioFollowersFriendsMax:
            attributsSus+=1
        if user["avg_hashtag"] > avgHashtagMax:
            attributsSus+=1
        if user["avg_url"] > avgUrlMax:
            attributsSus+=1
        if (attributsSus >= 3):
            rethinkDBservice.updateUser(user["id"], {"suspect": 1})
            nbSuspectTweets+=1
            print(nbSuspectTweets)
            # user['suspect'] = 1
        else:
            rethinkDBservice.updateUser(user["id"], {"suspect": -1})
            print(nbSuspectTweets)
            # user['suspect'] = 0





print(nbSuspectTweets)


