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
# shape = data.shape
# print(shape)

for i in data:


    cursor_user = r.db('IF29').table('tweets').filter({
        "user": {
                "screen_name": i
        }
    }).run()
    print(cursor_user)

    dates = []
    for t in cursor_user:
        date = t['created_date']
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        dates.append(date)
        print(date)
        
    serieDates = pd.Series(dates)
    # on compte le nombre d'occurence pour chaque jour
    frequency = np.mean(serieDates.dt.date.value_counts())
    print(frequency)
