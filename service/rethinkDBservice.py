from rethinkdb import r
from config import config
r.connect("151.80.149.147",28015,"IF29",user=config.RETHINKDB_USERNAME,password=config.RETHINKDB_PASSWORD).repl()

def getConnection():
    return r