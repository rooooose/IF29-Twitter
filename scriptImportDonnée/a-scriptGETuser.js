const fs = require('fs');
const readline = require('readline');

async function processLineByLine() {
    const fileStream = fs.createReadStream('./allTweets.json');
    
    const userList = [];

    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity
    });
    // Note: we use the crlfDelay option to recognize all instances of CR LF
    // ('\r\n') in input.txt as a single line break.
  
    let cmpt = 0

    for await (const line of rl) {
      ++cmpt;
      // Each line in input.txt will be successively available here as `line`.
      tweet = JSON.parse(line);
      if ( ! userList.includes(tweet.user.id) ) {
          userList.push(tweet.user.id)
          fs.appendFile('./allUser.json', '{"id": '+tweet.user.id+'}\n', function (err) {
            if (err) return console.log(err);
            console.log(cmpt);
          })
      }
    }

  }
  
  processLineByLine();