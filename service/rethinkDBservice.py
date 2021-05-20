from rethinkdb import r
from config import config
import pprint

dbName = "test"

r.connect("151.80.149.147",28015,dbName,user=config.RETHINKDB_USERNAME,password=config.RETHINKDB_PASSWORD).repl()

def getConnection():
    return r

def getUsersCursors():
    return r.db(dbName).table("users").run() 

def getTweetsByUserIdCursors(userId):
    return r.db(dbName).table("tweets").get_all(userId, index="user-id").run() 

def createData(table, data):
    r.db(dbName).table(table).insert(data).run()