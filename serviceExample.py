from service import rethinkDBservice
import pprint
import json

r = rethinkDBservice.getConnection()

cursor = r.db('IF29').table('tweets').get(1007083805889450000).run()

print(json.dumps(cursor, indent=4))

