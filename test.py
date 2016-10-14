from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants = db.participants
earlybirds = db.earlybirds

##def insert_bird(ec1, ec2, email, grade, gender, ranked_clubs, capt_email):
##    participant = {
##        "name": "",
##        "email": email,
##        "grade": grade,
##        "gender": gender,
##        "ec1": ec1,
##        "ec2": ec2,
##        "ranked_clubs": ranked_clubs,
##        "group": capt_email
##        }
##    earlybirds.insert(participant)
    
def insert_person(ec1, ec2, email, grade, gender, ranked_clubs, capt_email):
    participant = {
        "name": "",
        "email": email,
        "grade": grade,
        "gender": gender,
        "ec1": -1,
        "ec2": -1,
        "ranked_clubs": ranked_clubs,
        "group": capt_email
        }
    participants.insert(participant)

#if you have 15 TOTAL of something, you can have 4 in each group
    #2 of that thing in each group  -- 2+2 makes limit
    #3+2 doesn't work

def main():
    #club0 = [0, 0, 1, 1], [0, 2, 0], ec =none
    insert_person(34, 23, "group0@amherst.edu", 3, 1, [0, 1, 2, 3, 4], "group0@amherst.edu")
    insert_person(1, 16, "group01", 2, 1, [0, 1, 2, 3, 4], "group0@amherst.edu")
    #club2:  =  [0, 1, 0, 1], [0, 2, 0]
    insert_person(9, 23, "group2@amherst.edu", 3, 1, [2, 0, 1, 4, 3], "group2@amherst.edu")
    insert_person(12, 8, "group21", 1, 1, [2, 0, 1, 4, 3], "group2@amherst.edu")
    #club1 = [1, 0, 0, 2], [0, 3, 0]
    insert_person(6, 4, "group1@amherst.edu", 3, 1, [1, 2, 0, 3, 4],"group1@amherst.edu")
    insert_person(21, 17, "group12", 0, 1, [1, 2, 0, 3, 4], "group1@amherst.edu")
    insert_person(13, 14, "group13", 3, 1, [1, 2, 0, 3, 4], "group1@amherst.edu")
    #club3 = [1, 1, 0, 0], [0, 2, 0]
    insert_person(9, 23, "group3@amherst.edu", 0, 1, [3, 0, 1, 4, 2], "group3@amherst.edu")
    insert_person(12, 8, "group31", 1, 1, [3, 0, 1, 4, 2], "group3@amherst.edu")
    #club4 = [2, 0, 0, 1], [0, 3, 0]
    insert_person(9, 23, "group4@amherst.edu", 0, 1, [4, 0, 1, 2, 3], "group4@amherst.edu")
    insert_person(12, 8, "group41", 0, 1, [4, 0, 1, 2, 3], "group4@amherst.edu")
    insert_person(12, 8, "group42", 3, 1, [4, 0, 1, 2, 3], "group4@amherst.edu")
    
    #problematic Group 1 = [1, 0,  1, 1],  [0, 3, 0]
    insert_person(18, 19, "groupprob", 2, 1, [1, 2, 4, 3, 0], "capt@amherst.edu")
    insert_person(16, 17, "groupprob2", 3, 1, [1, 2, 4, 3, 0],"capt@amherst.edu")
    insert_person(14, 19, "capt@amherst.edu", 0, 1, [1, 2, 4, 3, 0], "capt@amherst.edu")

main()
