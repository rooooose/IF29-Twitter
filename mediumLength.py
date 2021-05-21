#longeur d'un seul tweet
from service import rethinkDBservice

r = rethinkDBservice.getConnection()

oneRaw = r.db('IF29').table('tweets').get(1007083805889450000)
print(oneRaw.run())
oneText = oneRaw.pluck('text').run()
#print(json.dumps(cursor, indent=4))
print(oneText)
longeur=len(oneText['text'])
print(longeur)
