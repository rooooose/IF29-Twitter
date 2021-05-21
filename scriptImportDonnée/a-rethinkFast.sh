#!/bin/bash

cat *.json >> allTweets.json

rethinkdb import -f allTweets.json --password-file a-pass.txt --table allData.tweets -c 151.80.149.147:28015 --format json --force

rethinkdb import -f allUser.json --password-file a-pass.txt --table allData.users -c 151.80.149.147:28015 --format json --force