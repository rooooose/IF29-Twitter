# Nombre moyen d'URLs, d'hashtag, de 'trends' et references dans les tweets
# maj : 20/05/21

# from service import rethinkDBservice
# import pprint
# import json
import numpy as np
# from datetime import datetime
# import pandas as pd


# r = rethinkDBservice.getConnection()

# # Récupère tous les noms d'utilisateurs
# users = rethinkDBservice.getUsersCursors()
# users = list(users)

def getURLCount(t):
    #url_count = t['entities']['urls']
    url_count = len(t['entities']['urls'])
    return url_count

def get_url_avg(u):
    # pour chaque utilisateur, on cherche toutes le nb de retweets sur ce qu'il a tweeté
    cursor_user = r.db('test').table('tweets').get_all(u["id"],index="userId").run()
    # cursor_user = r.db('IF29').table('tweets').get_all(u["id"],index="userId").run()

    cursor_user = list(cursor_user)

    url_count = [getURLCount(t) for t in cursor_user]
    print(url_count)

    avg_number_url = np.mean(url_count)
    # print(u, " : ", avg_number_url)
    file1 = open("retweet_count.csv","a")
    file1.write(str(u) +","+ str(avg_number_url)+"\n")
    file1.close()
    return avg_number_url

# L = [[u,get_url_avg(u)] for u in users]
# L = [[u,get_url_avg(u)] for u in users[10:15]]

def calcAvgUrl(tweets):
    url_count = [getURLCount(t) for t in cursor_user]
    avg_number_url = np.mean(url_count)
    return {"avg_number_url": avg_number_url}