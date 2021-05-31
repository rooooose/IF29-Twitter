# from service import rethinkDBservice
# import pprint

# users = rethinkDBservice.getUsersCursors()

def calcRateRepliedTweets(tweets):
  totalReplied = 0
  totalTweets = len(list(tweets))
  for tweet in tweets:
    if tweet['reply_count'] :
      print(tweet['reply_count'])
      totalReplied+=1
  res = totalReplied * 100 / totalTweets
  return res

# for user in users:
#     tweets = rethinkDBservice.getTweetsByUserIdCursors(user["id"])
#     result = calcRateRepliedTweets(tweets)
#     rethinkDBservice.updateUser(user["id"], result)
    # pprint.pprint(user)
    # pprint.pprint(result)
    # break