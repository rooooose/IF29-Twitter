from service import rethinkDBservice
from scriptCalcParam import agressiviteTweet
from scriptCalcParam import avgRetweetUrlHashtag
from scriptCalcParam import followers
from scriptCalcParam import mediumLengthTweet
from scriptCalcParam import repliedTweets
from scriptCalcParam import tweet_frequency
from scriptCalcParam import verified
from scriptCalcParam import visibility
import pprint
import json


users = rethinkDBservice.getUsersCursors()
cmp = 0
for user in users:
    if len(user) <= 1 :
        tweets = list(rethinkDBservice.getTweetsByUserIdCursors(user["id"]))

        if len(tweets) != 0:
            res = {
                "agressivite": agressiviteTweet.calcAgressiviteTweet(tweets),
                "avg_retweet": avgRetweetUrlHashtag.getRetweetAvg(tweets),
                "avg_url": avgRetweetUrlHashtag.getURLAvg(tweets),
                "avg_hashtag": avgRetweetUrlHashtag.getHashtagAvg(tweets),
                "rationFollowersFriends": followers.calcFollowers(tweets),
                "mediumLength": mediumLengthTweet.get_users_mediumLengthTweets(tweets),
                "rateOfRepliedTweets": repliedTweets.calcRateRepliedTweets(tweets),
                "tweet_per_day": tweet_frequency.calcTweetFrequency(tweets),
                "verified": verified.calcVerified(tweets),
                "visibility": visibility.calcVisibility(tweets),
                "version": "1"
            }
            rethinkDBservice.updateUser(user["id"], res)
            # pprint.pprint(res)
            # pprint.pprint(user)
            cmp+=1
            print(cmp)
            # if cmp > 1:
            #     break
