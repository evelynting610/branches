from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants = db.participants

def insert_person(email, grade, gender, ranked_clubs, ec1, capt_email):
    participant = {
        "name": "",
        "email": email,
        "grade": grade,
        "gender": gender,
        "ec1": ec1,
        "ec2": -1,
        "ranked_clubs": ranked_clubs,
        "group": capt_email
        }
    participants.insert(participant)

def main():
    #club0 = [1, 0, 1, 0], [2, 0, 0], ec =none
    insert_person("", 0, 0, [0, 1, 2], 8, "")
    insert_person("", 2, 0, [0, 1, 2], 8, "")
    #club2:  =  [1, 1, 0, 0], [2, 0, 0]
    insert_person("", 0, 0, [2, 1, 0], 10, "")
    insert_person("", 1, 0, [2, 1, 0], 24, "")
    #club1 = [0, 1, 1, 0], [1, 0, 1]
    insert_person("", 2, 0, [1, 2, 0], 13, "")
    insert_person("", 1, 2, [1, 2, 0], 26, "")
    #Entering Group = [1, 1,  1, 1],  [4, 0, 0]
    insert_person("capt@amherst.edu", 0, 0, [0, 1, 2], 3, "capt@amherst.edu")
    insert_person("a@amherst.edu", 1, 0, [0, 1, 2], 32, "capt@amherst.edu")
    insert_person("b@amherst.edu", 2, 0, [0, 1, 2], 21, "capt@amherst.edu")
    insert_person("c@amherst.edu", 3, 0, [0, 1, 2], 18, "capt@amherst.edu")

main()
