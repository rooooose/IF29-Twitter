from service import rethinkDBservice

r = rethinkDBservice.getConnection()

tweets = r.db("test").table("tweets").run()

for tweet in tweets:
    user = {
        "id": tweet["user"]["id"],
        "name": tweet["user"]['name']
    }
    userTest = r.db("test").table("users").get(789995).run()
    if not userTest:
        rethinkDBservice.createData('users', user)
    break

    