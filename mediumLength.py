#longeur d'un seul tweet
from service import rethinkDBservice

r = rethinkDBservice.getConnection()

oneRaw = r.db('IF29').table('tweets').get(1007083805889450000)
print(oneRaw.run())
exOneText = oneRaw.pluck('text').run()
#print(json.dumps(cursor, indent=4))
print(exOneText)
longeur=len(exOneText['text'])
print(longeur)

oneRaw = r.db('IF29').table('tweets').get()
print(oneRaw.run())
exOneText = oneRaw.pluck('text').run()
#print(json.dumps(cursor, indent=4))
print(exOneText)
longeur=len(exOneText['text'])
print(longeur)
