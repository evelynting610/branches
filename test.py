from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants = db.participants

def insert_person(ec1, ec2, email, grade, gender, ranked_clubs, capt_email):
    participant = {
        "name": "",
        "email": email,
        "grade": grade,
        "gender": gender,
        "ec1": ec1,
        "ec2": ec2,
        "ranked_clubs": ranked_clubs,
        "group": capt_email
        }
    participants.insert(participant)

def main():
    #club0 = [0, 0, 1, 1], [0, 2, 0], ec =none
    insert_person(34, 23, "group0@amherst.edu", 3, 1, [0, 1, 2], "group0@amherst.edu")
    insert_person(1, 16, "group01", 2, 1, [0, 1, 2], "group0@amherst.edu")
    #club2:  =  [0, 1, 0, 1], [0, 2, 0]
    insert_person(9, 23, "group2@amherst.edu", 3, 1, [2, 0, 1], "group2@amherst.edu")
    insert_person(12, 8, "group21", 1, 1, [2, 0, 1], "group2@amherst.edu")
    #club1 = [0, 0, 0, 3], [1, 1, 1]
    insert_person(6, 4, "group1@amherst.edu", 3, 0, [1, 2, 0],"group1@amherst.edu")
    insert_person(21, 17, "group12", 3, 1, [1, 2, 0], "group1@amherst.edu")
    insert_person(13, 14, "group13", 3, 2, [1, 2, 0], "group1@amherst.edu")
    #problematic Group 1 = [1, 1,  1, 1],  [0, 4, 0]
    insert_person(15, 16, "group31", 1, 1, [0, 1, 2], "capt@amherst.edu")
    insert_person(18, 19, "group32", 2, 1, [0, 1, 2], "capt@amherst.edu")
    insert_person(16, 17, "group33", 3, 1, [0, 1, 2],"capt@amherst.edu")
    insert_person(14, 19, "capt@amherst.edu", 0, 1, [0, 1, 2], "capt@amherst.edu")

main()
