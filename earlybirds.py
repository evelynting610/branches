from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants=db.participants
earlybirds = db.earlybirds

bird_emails = ["wwood18@amherst.edu",
"awen19@amherst.edu",
"prose18@amherst.edu",
"hcrosbiefoote18@amherst.edu",
"bcook16@amherst.edu", "rbarasch19@amherst.edu", "jmichael19@amherst.edu", "jmayer18@amherst.edu",
"chiuhu17@amherst.edu",
"lkim19@amherst.edu",
"ydiaz18@amherst.edu",
"ahealey19@amherst.edu",
"bgreene18@amherst.edu",
"msantamaria18@amherst.edu", "areczek18@amherst.edu"]

for bird_email in bird_emails:
    bird = participants.find_one({"email" : bird_email})
    if bird==None:
        print("No form for early bird ", bird_email)
    else:
        earlybirds.insert_one(bird)
        participants.delete_one({"email" : bird_email})
  

