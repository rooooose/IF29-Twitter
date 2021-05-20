from service import rethinkDBservice

users = rethinkDBservice.getUsersCursors()

for user in users:
    tweets = rethinkDBservice.getTweetsByUserIdCursors(user["id"])
    result = calcRateRepliedTweets(tweets)
    pprint.pprint(result)
    # rethinkDBservice.updateUser(user["id"], {"resultat": 45, "resultat2": 46})
    break

def calcRateRepliedTweets(tweets):
  
