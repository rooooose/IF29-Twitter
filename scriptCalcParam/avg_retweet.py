# Nombre moyen de retweet
# maj : 17/05/21

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

def getRetweetCount(t):
    retweet_count = t['retweet_count']
    return retweet_count

def get_retweet_avg(u):
    # pour chaque utilisateur, on cherche toutes le nb de retweets sur ce qu'il a tweeté
    cursor_user = r.db('test').table('tweets').get_all(u["id"],index="userId").run()
    # cursor_user = r.db('IF29').table('tweets').get_all(u["id"],index="userId").run()

    cursor_user = list(cursor_user)

    retweet_count = [getRetweetCount(t) for t in cursor_user]
    print(retweet_count)

    avg_retweet = np.mean(retweet_count)
    # if (avg_retweet > 0):
    #     print(u, " : ", avg_retweet)
    file1 = open("retweet_count.csv","a")
    file1.write(str(u) +","+ str(avg_retweet)+"\n")
    file1.close()
    return avg_retweet

L = [[u,get_retweet_avg(u)] for u in users[:4]]