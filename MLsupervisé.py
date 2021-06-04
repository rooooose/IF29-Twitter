from service import rethinkDBservice

users = rethinkDBservice.getUsersCursors()

for user in users:
    if(user["verified"]):
        rethinkDBservice.updateUser(user["id"], {"suspect": -1})