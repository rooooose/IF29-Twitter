# from service import rethinkDBservice
# import pprint

# users = rethinkDBservice.getUsersCursors()

def calcAgressiviteTweet(tweets):
  tweets = sorted(list(tweets), key=lambda tweet: tweet['timestamp_ms'])
  lastTweetFriends = None
  totalFriendsVariation = 0
  totalTweets = len(tweets)
  for tweet in tweets:
    tweeterFriends = tweet['user']['followers_count']
    if not lastTweetFriends:
      lastTweetFriends = tweeterFriends
    else:
      totalFriendsVariation+=tweeterFriends-lastTweetFriends
      lastTweetFriends=tweeterFriends
  res = totalFriendsVariation/totalTweets
  return {'agressivite': res}

# for user in users:
#     tweets = rethinkDBservice.getTweetsByUserIdCursors(user["id"])
#     result = agressiviteTweet(tweets)
#     # pprint.pprint(user)
#     # pprint.pprint(result)
#     rethinkDBservice.updateUser(user["id"], result)
