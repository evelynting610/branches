from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants = db.participants2
entries = db.entries
groups = db.groups

entries.delete_many({})
groups.delete_many({})

for p in participants.find():
    pemail = p['email']
    captain_email = p['group']
    
    if entries.find_one({"email" : pemail}) != None:
        print (pemail, "has been entered twice")

    if (p['ec1']==p['ec2']) and p['ec1']!="-1":
        print (pemail, " messed up ecs")

    if captain_email != "":
        group_doc = entries.find_one({ "captain_email" : captain_email})
        if group_doc != None:
            member_list = group_doc['member_list']
            if len(member_list)==3:  #This number may change
                print("Sorry, ", pemail, " already 3 people in that group")
            member_list.append(pemail)
            entries.update_one( {"captain_email" : captain_email}, {'$set': {"member_list": member_list}})
            groups.update_one( {"captain_email" : captain_email}, {'$set': {"member_list": member_list}})
        else:
            entries.insert({ "captain_email" : captain_email, "member_list" : [pemail] })
            numingroup = int(p['num_in_group'])
            groups.insert({ "captain_email" : captain_email, "member_list" : [pemail], "numingroup" : numingroup })

        if participants.find_one({"email" : captain_email }) == None:
            print("Captain ", captain_email, " is not in database")
            print("group member is ", pemail)
            
    entries.insert({"email" : pemail})

for g in groups.find():
    num_members = len(g['member_list'])
    numingroup = g['numingroup']

    if num_members!=numingroup:
        print("group ", g['captain_email'], " has ", num_members, " not ", numingroup)
