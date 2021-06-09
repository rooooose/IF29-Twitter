from scriptCalcParam import agressiviteTweet
from scriptCalcParam import avgRetweetUrlHashtag
from scriptCalcParam import followers
from scriptCalcParam import mediumLengthTweet
from scriptCalcParam import repliedTweets
from scriptCalcParam import tweet_frequency
from scriptCalcParam import verified
from scriptCalcParam import visibility
from scriptCalcParam import ageAccount
import pprint
import json

file1 = open('./data/a-DATA.json', 'r')
Lines = file1.readlines()
print('chargement ok')
tweetByuser = {} 

count = 0
for line in Lines:
    count += 1
    if count%10000 == 0:
        print(count)
    if count == 100000:
        break
    tweet = json.loads(line)
    userId = tweet["user"]["id"]
    if not userId in tweetByuser:
        tweetByuser[userId] = {
            "tweets": [tweet]
        }
    else:
        tweetByuser[userId]["tweets"].append(tweet)

print('tweetbyuser ok')

cmp = 0

for userId in tweetByuser:
    tweets = tweetByuser[userId]["tweets"]
    # print(tweets)

    if len(tweets) != 0:
        res = {
            "id": userId,
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
            "accountAge(days)": ageAccount.get_age_account(tweets),
            "version": "1"
        }
        cmp+=1
        if cmp%10000 == 0:
            print(cmp)
        with open('./result3M.json', 'a') as the_file:
            the_file.write(json.dumps(res)+'\n')

print("fin")
