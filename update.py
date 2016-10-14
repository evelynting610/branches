from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants=db.participants2
copy = db.copy2

##participants.update_one( {"email" : "afrenett18@amherst.edu"}, {'$set': {"group":"afrenett18@amherst.edu"}})
##participants.update_one( {"email" : "cnkansahsiriboe18@amherst.edu"}, {'$set': {"group":"cnkansahsiriboe18@amherst.edu"}})
##participants.update_one({"email": "atemares18@amherst.edu"}, {'$set': {"num_in_group": 3}})

participant = {
    "name": "Kali Robinson",
    "email": "krobinson17@amherst.edu",
    "grade": "0",
    "gender": "2",
    "ec1": "71",
    "ec2": "50",
    "ranked_clubs": [0, 1, 2, 3, 4, 5],
    "num_in_group": "2",
    "group": "kblake17@amherst.edu"
    }
participants.insert(participant)
copy.insert(participant)

participants.update_one( {"email" : "kblake17@amherst.edu"}, {'$set': {"group":"kblake17@amherst.edu", "num_in_group": "2"}})
copy.update_one( {"email" : "kblake17@amherst.edu"}, {'$set': {"group":"kblake17@amherst.edu", "num_in_group": "2"}})

##names = open("names.txt", 'w')
##
##for p in participants.find():
##    name = p['name']+"\n"
##    names.write(name)
##
##names.close()
