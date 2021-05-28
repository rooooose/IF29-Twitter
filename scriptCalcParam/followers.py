from service import rethinkDBservice
import pprint
import json
import numpy as np

r = rethinkDBservice.getConnection()

# data = np.loadtxt('./IF29-Twitter/users.txt', dtype='str', delimiter=' ')
users = rethinkDBservice.getUsersCursors()

# cursor = r.db('IF29').table('tweets').run()
def get_users_followers(u):
    r.db('test').table("users").get(u['id']).replace(r.row.without('ratio')).run() 
    
    # tweet = rethinkDBservice.getLastTweetByUserIdCursors(u["id"])
    # # cursor_user = r.table('tweets').get_all(u,index="userScreenName").nth(-1).run()

    # followers = tweet['user']['followers_count']
    # friends = tweet['user']['friends_count']
    # screen_name = tweet['user']['screen_name']
    # ratio=0
    # if friends != 0:
    #     ratio = followers/friends
    # print(print(u['name'], " : ", ratio))
    # rethinkDBservice.updateUser(u["id"], {'followers':followers, 'friends':friends, 'ratio_frds_flwrs' : ratio})

L = [get_users_followers(u) for u in users]

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

