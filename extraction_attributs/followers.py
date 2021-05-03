import json

# class User:
#     def __init__(self, followers):
#         self.followers = followers



with open("IF29-Twitter\\extraction_attributs\\raw0.json", encoding="utf8") as json_file:
    tweets = []
    users = []
    for line in json_file:
        tweets.append(json.loads(line))

    for u in tweets:
        followers = u['user']['followers_count']
        friends = u['user']['friends_count']
        # print('Followers: ' , u['user']['followers_count'])
        # users.append(User(followers))
        ratio=0
        if friends != 0:
            ratio = followers/friends
        users.append([followers,friends,ratio])

# Si le ratio est plus petit que 1, alors le user suit plus de personnes qu'il n'a de followers (=> profil suspect)
print(users)

