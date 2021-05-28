# from service import rethinkDBservice
# r = rethinkDBservice.getConnection()

#Récupération de la liste des utilisateurs
# users = list(rethinkDBservice.getUsersCursors())
    
#Calcule la visibilité d'un utilisateur
def get_visibility(user):
    userId = user["id"]
    tweets = list(rethinkDBservice.getTweetsByUserIdCursors(userId))

    costMention = 11.4 #C(@)
    costHashtag = 11.6 #C(#)
    
    nbMention = 0
    nbHashtag = 0

    for t in tweets:
        text = t["text"]
        nbMention += text.count("@")
        nbHashtag += text.count("#")
    
    avgMention = nbMention/len(tweets) * costMention
    avgHashtag = nbHashtag/len(tweets) * costHashtag
    visibility = ( avgMention + avgHashtag ) / 280

    return visibility

# for user in users:
#     rethinkDBservice.updateUser(user["id"],  {"visibility" : get_visibility(user) } )
    #print(user["id"],get_visibility(user))

def calcVisibility(tweets):
    costMention = 11.4 #C(@)
    costHashtag = 11.6 #C(#)
    
    nbMention = 0
    nbHashtag = 0

    for t in tweets:
        text = t["text"]
        nbMention += text.count("@")
        nbHashtag += text.count("#")
    
    avgMention = nbMention/len(tweets) * costMention
    avgHashtag = nbHashtag/len(tweets) * costHashtag
    visibility = ( avgMention + avgHashtag ) / 280

    return {"visibility": visibility}