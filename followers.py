from service import rethinkDBservice
import pprint
import json

r = rethinkDBservice.getConnection()

cursor = r.db('IF29').table('tweets').pluck({'user':['followers_count', 'friends_count']}).run()

users = []
for u in cursor:
    followers = u['user']['followers_count']
    friends = u['user']['friends_count']
    ratio=0
    if friends != 0:
        ratio = followers/friends
    users.append([followers,friends,ratio])

print(users)

# with open("IF29-Twitter\\extraction_attributs\\raw0.json", encoding="utf8") as json_file:
#     tweets = []
#     users = []
#     for line in json_file:
#         tweets.append(json.loads(line))

#     for u in tweets:
#         followers = u['user']['followers_count']
#         friends = u['user']['friends_count']
#         # print('Followers: ' , u['user']['followers_count'])
#         # users.append(User(followers))
#         ratio=0
#         if friends != 0:
#             ratio = followers/friends
#         users.append([followers,friends,ratio])

# # Si le ratio est plus petit que 1, alors le user suit plus de personnes qu'il n'a de followers (=> profil suspect)
# print(users)

