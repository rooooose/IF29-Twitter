from service import rethinkDBservice

r = rethinkDBservice.getConnection()

data = r.db("test").table("tweets").run()

for doc in data:
    user = {
        "id": doc["user"]["id"],
        "name": doc["user"]['name']
    }
    userTest = r.db("test").table("users").get_all(doc["user"]["id"], index='id').run()
    if not list(userTest):
        rethinkDBservice.createData('users', user)

    