from service import rethinkDBservice

users = rethinkDBservice.getUsersCursors()

ageMax = 200
agressiviteMax = 10
visibilityMax = 0.3
tweetsPerDayMax = 15
ratioFollowersFriendsMax = 0.1
avgHashtagMax = 0.3
avgUrlMax = 1.5

nbSuspectTweets = 0
for user in users:
#    if(user["verified"]):
#        rethinkDBservice.updateUser(user["id"], {"suspect": -1})
    if (not user["verified"]):    
        if (user["accountAge(days)"] < 200 and user["agressivite"] > agressiviteMax and user["visibility"] > visibilityMax and user["tweet_per_day"] > tweetsPerDayMax and user["rationFollowersFriends"] < ratioFollowersFriendsMax and user["avg_hashtag"] > avgHashtagMax and user["avg_url"] > avgUrlMax):
            #rethinkDBservice.updateUser(user["id"], {"suspect": 1})
            nbSuspectTweets+=1

print(nbSuspectTweets)
