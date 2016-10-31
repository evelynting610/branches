from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.branches
participants=db.f16participants

participants.update_one( {"email" : "mscala19@amherst.edu"}, {'$set': {"num_in_group": 2}})
participants.update_one( {"email" : "ehollenberg19@amherst.edu"}, {'$set': {"num_in_group": 2, "group":"ehollenberg19@amherst.edu"}})
# participants.update_one({"group": "ehong20@amherst.edu"}, {'$set': {"num_in_group": 3}})
# participants.update_one({"group": "kstanton18@amherst.edu"}, {'$set': {"num_in_group": 3}})

# participant = {
#     "name": "Kali Robinson",
#     "email": "krobinson17@amherst.edu",
#     "grade": "0",
#     "gender": "2",
#     "ec1": "71",
#     "ec2": "50",
#     "ranked_clubs": [0, 1, 2, 3, 4, 5],
#     "num_in_group": "2",
#     "group": "kblake17@amherst.edu"
#     }
# participants.insert(participant)
# copy.insert(participant)

# participants.update_one( {"email" : "kblake17@amherst.edu"}, {'$set': {"group":"kblake17@amherst.edu", "num_in_group": "2"}})
# copy.update_one( {"email" : "kblake17@amherst.edu"}, {'$set': {"group":"kblake17@amherst.edu", "num_in_group": "2"}})

##names = open("names.txt", 'w')
##
##for p in participants.find():
##    name = p['name']+"\n"
##    names.write(name)
##
##names.close()
