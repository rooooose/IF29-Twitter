# Nombre moyen d'URLs, d'hashtag, de 'trends' et references dans les tweets
# maj : 20/05/21

from service import rethinkDBservice
import pprint
import json
import numpy as np
from datetime import datetime
import pandas as pd


r = rethinkDBservice.getConnection()

# Récupère tous les noms d'utilisateurs
users = rethinkDBservice.getUsersCursors()
users = list(users)

def getURLAvg(tweets):
    url_count = []
    for t in tweets:
        url_count.append(len(t['entities']['urls']))
    print(url_count)
    avg_number_url = np.mean(url_count)
    return avg_number_url

def getHashtagAvg(tweets):
    hashtag_count = []
    for t in tweets:
        hashtag_count.append(len(t['entities']['hashtags']))
    print(hashtag_count)
    avg_number_hashtag = np.mean(np.array(hashtag_count))
    return avg_number_hashtag

def getRetweetAvg(tweets):
    retweet_count = []
    for t in tweets:
        retweet_count.append(t['retweet_count'])
    print(retweet_count)
    avg_retweet = np.mean(np.array(retweet_count))
    return avg_retweet


for u in users:
    # pour chaque utilisateur, on cherche le nb de retweets sur ce qu'il a tweeté
    tweets = r.db('test').table('tweets').get_all(u["id"],index="userId").run()
    # tweets = rethinkDBservice.getTweetsByUserIdCursors(u["id"])
    tweets = list(tweets)
    # nombre moyen d'hashtags
    avg_hashtag = getHashtagAvg(tweets)
    # nombre moyen d'url
    avg_url = getURLAvg(tweets)
    # nombre moyen de retweet
    avg_retweet = getRetweetAvg(tweets)
    #print(u, " - avg retweet :  ", avg_retweet, " - avg url : ", avg_url, " - avg hashtags : ", avg_hashtag)
    # update table users
    rethinkDBservice.updateUser(u["id"], {"avg_retweet": avg_retweet, "avg_hashtag": avg_hashtag, "avg_url": avg_url})