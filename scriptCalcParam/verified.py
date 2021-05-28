from service import rethinkDBservice
r = rethinkDBservice.getConnection()

users = list(rethinkDBservice.getUsersCursors())

def is_verified(user):
    userId = user["id"]
    tweets = list(rethinkDBservice.getTweetsByUserIdCursors(userId))
    verified = False
    for t in tweets:
        if t["user"]["verified"]:
            verified = True
    return verified

for user in users:
    rethinkDBservice.updateUser(user["id"],  {"verified" : is_verified(user) } )