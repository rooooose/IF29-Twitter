from rethinkdb import r
from config import config
import pprint

dbName = "allData"
dbUserTable = "users"

r.connect("151.80.149.147",28015,dbName,user=config.RETHINKDB_USERNAME,password=config.RETHINKDB_PASSWORD).repl()

def getConnection():
    return r

def getUsersCursorsVersion(version):
    return r.db(dbName).table(dbUserTable).filter(r.row["version"] != version).run() 

def getUsersCursors():
    return r.db(dbName).table(dbUserTable).has_fields('agressivite').run() 

def getTweetsByUserIdCursors(userId):
    return r.db(dbName).table("tweets").get_all(userId, index="userId").run() 

def getLastTweetByUserIdCursors(userId):
    return r.db(dbName).table("tweets").get_all(userId, index="userId").nth(-1).run() 

def createData(table, data):
    r.db(dbName).table(table).insert(data).run()

def updateUser(id, data):
    r.db(dbName).table(dbUserTable).get(id).update(data).run()