const fs = require('fs');
const readline = require('readline');

async function processLineByLine() {
    const fileStream = fs.createReadStream('./allTweets.json');
    
    const tweetsByUser = {};

    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity
    });
  
    let cmpt = 0

    for await (const line of rl) {
      ++cmpt;
      if (cmpt == 10) break
      if (cmpt%10000 == 0) console.log(cmpt);
      // Each line in input.txt will be successively available here as `line`.
      let tweet = JSON.parse(line);
      let tweet2 = {
        "user": {
          "id": tweet.user.id,
          "created_at": tweet.user.created_at,
          "followers_count": tweet.user.followers_count,
          "friends_count": tweet.user.friends_count,
          "verified": tweet.user.verified,
        },
        "entities" : {
          "urls": tweet.entities.urls,
          "hashtags": tweet.entities.hashtags,
        },
        "text": tweet.text,
        "retweet_count": tweet.retweet_count,
        "reply_count": tweet.reply_count,
        "created_date": tweet.created_date,
        "timestamp_ms": tweet.timestamp_ms,
      }

      fs.appendFile('./a-DATA.json', JSON.stringify(tweet2)+"\n", function (err) {
        if (err) return console.log(err);
      })
    }

  }
  
  processLineByLine();