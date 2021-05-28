from service import rethinkDBservice
# import pprint
# import json


# r = rethinkDBservice.getConnection()
# users = rethinkDBservice.getUsersCursors()

def getLength(t):
        l = len(t['text'])
        return l

def get_users_mediumLengthTweets(u):

    tweets = rethinkDBservice.getTweetsByUserIdCursors(u["id"])

    lengths = [getLength(t) for t in tweets]
    somme=0
    for l in lengths:
       somme = somme + l
    return somme
    nbTweets = len(tweets)
    mediumLength = somme/nbTweets
    
    rethinkDBservice.updateUser(u["id"], {"medium_length_by_tweet": mediumLength})

# L = [get_users_mediumLengthTweets(u) for u in users]    

def calcMediumLengthTweet(tweets):
    lengths = [getLength(t) for t in tweets]
    somme=0
    for l in lengths:
       somme = somme + l
    nbTweets = len(tweets)
    mediumLength = somme/nbTweets
    return {"mediumLength": mediumLength}