from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants = db.participants


_301 = [0, 0, 0, 0, 0]
ailurus = [0, 0, 0, 0, 0]
buenavista = [0, 0, 0, 0, 0]
fourthwall = [0, 0, 0, 0, 0]
sos = [0, 0, 0, 0, 0]

for p in participants.find():
    clublist = p['ranked_clubs']

    if len(clublist)<5:
        print ("email of participant is ", p['email'])
    for ix in range(0, len(clublist)):
        club = clublist[ix]
        if club==0:
            _301[ix]+=1
        elif club==1:
            ailurus[ix]+=1
        elif club==2:
            buenavista[ix]+=1
        elif club==3:
            if ix==0:
                ranked_clubs = p['ranked_clubs']
                print (p['email'], "' second choice is ", ranked_clubs[1])
            fourthwall[ix]+=1
        else:
            sos[ix]+=1

print("301 ", _301)
print("ailurus ", ailurus)
print("buenavista ", buenavista)
print("fourthwall ", fourthwall)
print("sos ", sos)
            
