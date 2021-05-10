from service import rethinkDBservice
import pprint
import json
import numpy as np

r = rethinkDBservice.getConnection()

data = np.loadtxt('./IF29-Twitter/users.txt', dtype='str', delimiter=' ')

# cursor = r.db('IF29').table('tweets').run()
def get_users_followers(u):
    cursor_user = r.table('tweets').get_all(u,index="userScreenName").nth(-1).run()

    # for t in cursor_user:
    followers = cursor_user['user']['followers_count']
    friends = cursor_user['user']['friends_count']
    screen_name = cursor_user['user']['screen_name']
    ratio=0
    if friends != 0:
        ratio = followers/friends
    print(print(screen_name, " : ", ratio))
    file1 = open("./IF29-Twitter/followers.csv","a")
    file1.write(str(screen_name) +","+ str(followers)+","+ str(friends)+","+ str(ratio)+"\n")
    file1.close()
    # r.table('users').get(u).update({'followers':followers}, {'friends':friends}, {'ratio' : ratio}).run()

L = [get_users_followers(u) for u in data[np.where(data=='torrente55')[0][0]:]]

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

