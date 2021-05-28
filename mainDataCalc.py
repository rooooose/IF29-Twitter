from service import rethinkDBservice
from scriptCalcParam import agressiviteTweet

users = rethinkDBservice.getUsersCursors()

for user in users:
    tweets = rethinkDBservice.getTweetsByUserIdCursors(user["id"])

    res = [
        agressiviteTweet.agressiviteTweet(tweets),
        
    ]
    # rethinkDBservice.updateUser(user["id"], res)
    pprint.pprint(res)
    break