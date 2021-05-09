from service import rethinkDBservice
import pprint
import json
import numpy as np
from datetime import datetime
import pandas as pd

r = rethinkDBservice.getConnection()


# Récupère tous les noms d'utilisateurs

# cursor = r.db('IF29').table('tweets').pluck({'user':'screen_name'}).run()
# users = []

# for u in cursor:
#     user = u['user']['screen_name']
#     users.append(user)

# users = list(dict.fromkeys(users))
# print(users)

# np.savetxt('users.txt', users, delimiter=' ', fmt="%s")

data = np.loadtxt('./IF29-Twitter/users.txt', dtype='str', delimiter=' ')

def getDates(t):
        date = t['created_date']
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        # print(date)
        return date

def get_users_freq(u):
    # pour chaque utilisateur, on cherche toutes les dates auxquelles il a tweeté
    cursor_user = r.table('tweets').get_all(u,index="userScreenName").run()
    # cursor_user = r.db('IF29').table('tweets').get_all('user')(i, index='screen_name').run()
    # print(cursor_user)

    dates = [getDates(t) for t in cursor_user]
    # print(dates)
        
    serieDates = pd.Series(dates)
    # on compte le nombre d'occurences pour chaque jour
    frequency = np.mean(serieDates.dt.date.value_counts())
    print(u, " : ", frequency)
    file1 = open("tweet_per_day.csv","a")
    file1.write(str(u) +","+ str(frequency)+"\n")
    file1.close()
    return frequency
    # r.table('users').get(u).update({'tweet_per_day':frequency}).run()

L = [[u,get_users_freq(u)] for u in data[np.where(data=='torrente55')[0][0]:]]
# np.savetxt('tweet_per_day.csv', L, delimiter=',', fmt="%s")





# for i in data[np.where(data=='snna_x')[0][0]:]:
#     # pour chaque utilisateur, on cherche toutes les dates auxquelles il a tweeté
#     cursor_user = r.db('IF29').table('tweets').filter({
#         "user": {
#             "screen_name": i
#         }
#     }).run()
#     # cursor_user = r.db('IF29').table('tweets').get_all('user')(i, index='screen_name').run()
#     print(cursor_user)

#     def getDates(t):
#         date = t['created_date']
#         date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
#         print(date)
#         return date
    
#     dates = [getDates(t) for t in cursor_user]
#     print(dates)
    
#     # for t in cursor_user:
#     #     date = t['created_date']
#     #     print(date)
#     #     date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
#     #     print(date)
#     #     dates.append(date)
#     #     print(dates)
        
        
#     serieDates = pd.Series(dates)
#     # on compte le nombre d'occurences pour chaque jour
#     frequency = np.mean(serieDates.dt.date.value_counts())
#     print(i, " : ", frequency)
#     r.table('users').get(i).update({'tweet_per_day':frequency}).run()
