from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants=db.participants
earlybirds = db.earlybirds
fourthwall = db.fourthwall

for e in earlybirds.find():
    fourthwall.insert_one(e)
    newlist = [0, 0, 0, 0]
    email = e['email']
    clublist = e['ranked_clubs']
    new_ix = 0
    
    for ix in range(5):
        club = clublist[ix]
        if club==3:
            pass
        elif club >3:
            newlist[new_ix]=club-1
            new_ix+=1
        else:
            newlist[new_ix]=club
            new_ix+=1
            
    fourthwall.update_one( {"email" : email}, {'$set': {"ranked_clubs": newlist}})
        

for p in participants.find():
    fourthwall.insert_one(p)
    newlist = [0, 0, 0, 0]
    email = p['email']
    clublist = p['ranked_clubs']
    new_ix = 0
    
    for ix in range(5):
        club = clublist[ix]
        if club==3:
            pass
        elif club >3:
            newlist[new_ix]=club-1
            new_ix+=1
        else:
            newlist[new_ix]=club
            new_ix+=1
    fourthwall.update_one( {"email" : email}, {'$set': {"ranked_clubs": newlist}})
    
