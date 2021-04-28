from service import mongoDBService
import pprint

# Affiche un tweet
pprint.pprint(mongoDBService.findOne())
# Affiche juste le texte d'un tweet
pprint.pprint(mongoDBService.findOne()['text'])
# Recherche juste un tweet
pprint.pprint(mongoDBService.findOne({"lang":"pt"}))
# Recherche plusieur tweets
pprint.pprint(mongoDBService.find({"lang":"pt"})[0])

