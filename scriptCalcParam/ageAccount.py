"""
Age d'un compte. 
"""
# from service import rethinkDBservice
from datetime import datetime

# users = list(rethinkDBservice.getUsersCursors())
# tweets = list(rethinkDBservice.getTweetsByUserIdCursors(789995))

def get_age_account(tweets):
    creationDate0 = tweets[0]['user']['created_at']
    creationDate1 =  datetime.strftime(datetime.strptime(creationDate0,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d')
    creationDate2 = datetime.strptime(creationDate1, '%Y-%m-%d').date()
    
    td = datetime.date(datetime.now())
    
    accountAge = (td - creationDate2).days
    #Y = age // 365
    #reste = age % 365
    
    #M = reste // 31
    #D = reste % 31
    
    #accountAge = [Y, M, D]
    return accountAge

# for user in users:
#     tweets = list(rethinkDBservice.getTweetsByUserIdCursors(user["id"]))
#     result = get_age_account(user)
#     rethinkDBservice.updateUser(user["id"], result)
#     print(result)
