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
    return r.db(dbName).table("tweets").get_all(userId, index="userId").run() 

def createData(table, data):
    r.db(dbName).table(table).insert(data).run()

def updateUser(id, data):
    r.db(dbName).table('users').get(id).update(data).run()