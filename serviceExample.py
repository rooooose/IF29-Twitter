from service import rethinkDBservice
import pprint
import json

r = rethinkDBservice.getConnection()

# cursor = r.db('IF29').table('tweets').get(1007083805889450000).run()
# cursor = r.db('IF29').table('tweets').pluck({'user':['followers_count', 'friends_count']}).run()
# print(json.dumps(cursor, indent=4))


users = rethinkDBservice.getUsersCursors()

for user in users:
    tweets = rethinkDBservice.getTweetsByUserIdCursors(user["id"])
    pprint.pprint(list(tweets))
    # calcul resultat
    rethinkDBservice.updateUser(user["id"], {"resultat": 45, "resultat2": 46})
    break