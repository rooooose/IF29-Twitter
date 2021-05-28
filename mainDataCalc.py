from service import rethinkDBservice
from scriptCalcParam import agressiviteTweet
from scriptCalcParam import avg_retweet
from scriptCalcParam import avg_url
from scriptCalcParam import followers
from scriptCalcParam import mediumLengthTweet
from scriptCalcParam import repliedTweets
from scriptCalcParam import tweet_frequency
from scriptCalcParam import verified
from scriptCalcParam import visibility


users = rethinkDBservice.getUsersCursors()

for user in users:
    tweets = rethinkDBservice.getTweetsByUserIdCursors(user["id"])

    res = [
        agressiviteTweet.calcAgressiviteTweet(tweets),
        avg_retweet.calcAvgRetweet(tweets),
        avg_url.calcAvgUrl(tweets),
        followers.calcFollowers(tweets),
        mediumLengthTweet.calcMediumLengthTweet(tweets),
        repliedTweets.calcRateRepliedTweets(tweets),
        tweet_frequency.calcTweetFrequency(tweets),
        verified.calcVerified(tweets),
        visibility.calcVisibility(tweets),
    ]
    # rethinkDBservice.updateUser(user["id"], res)
    pprint.pprint(res)
    break