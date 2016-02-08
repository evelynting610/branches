from flask import Flask, request, session, g, redirect, url_for, abort, render_template
from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants = db.participants
users = db.users

# creates the application
app= Flask(__name__)
#application.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

##users = set()
##groups = dict()
error_message= ""

@app.route('/')
def starting_page():
    global error_message
    error_message=""
    return render_template('index.html', error_message=error_message)

#This info could all be gotten from Mongo
def isValid(email, captain_email):
    global error_message
    username_end = len(email)-12
    username = email[0 : username_end]

    if users.find_one({ "username" : username}) != None:
        error_message+="You already have a form on file.  Please contact the Branches Work Group if you would like to remove your former entry and resubmit"
        return False
    else:
        print(username)
        users.insert({"username" : username})
        
    if captain_email != "":
        group_doc = users.find_one({ "captain_email" : captain_email})
        if group_doc != None:
            member_list = group_doc['member_list']
            if len(member_list)==3:  #This number may change
                error_message+="Sorry.  There are already 3 people in that group"
                return False
            member_list.append(username)
            users.update_one( {"captain_email" : captain_email}, {'$set': {"member_list": member_list}})
        else:
            users.insert({ "captain_email" : captain_email, "member_list" : [username] })
    return True

@app.route('/completed', methods = ['POST'])
def insert_participant():
    global error_message
    error_message=""
    email = request.form['email']
    captain = request.form['captain']
    if isValid(email, captain):
        rank_dict = dict()
        for i in range(0, 3):
            key = request.form[str(i)]
            rank_dict[key] = i
        participant = {
            "name": request.form['name'],
            "email": email,
            "grade": request.form['class'],
            "gender":request.form['gender'],
            "ec1":request.form['ec1'],
            "ec2": request.form['ec2'],
            "ranked_clubs": [rank_dict['0'], rank_dict['1'], rank_dict['2']],
            "group": captain
            }
        participants.insert(participant)
        return render_template('completed.html')
    else:
        return render_template('index.html', error_message = error_message)

if __name__ == '__main__':
    app.debug=True          #restarts every time you change code
    app.run()
