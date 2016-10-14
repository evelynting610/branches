from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
ndb = client.branches
copy = ndb.s16participants
participants=db.participants
earlybirds = db.earlybirds
participants2 = db.participants2


for e in earlybirds.find():
     copy.insert_one(e)
for p in participants.find():
     copy.insert_one(p)
for p in participants2.find():
     copy.insert_one(p)
