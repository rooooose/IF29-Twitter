from service import rethinkDBservice

# users = rethinkDBservice.getUsersCursors()

def get_users_mediumLengthTweets(tweets):
    lSum = 0
    for t in tweets:
        l = len(t['text'])
        lSum = lSum + l
    nbTweets = len(tweets)
    mediumLength = round(lSum / nbTweets)
    return mediumLength

# for user in users:
#     tweets = list(rethinkDBservice.getTweetsByUserIdCursors(user["id"]))
#     result = get_users_mediumLengthTweets(tweets)
#     rethinkDBservice.updateUser(user["id"], result)
