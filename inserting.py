from flask import Flask, request, session, g, redirect, url_for, abort, render_template
from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants = db.participants

# creates the application
app= Flask(__name__)
#application.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

users = set()
groups = dict()
error_message= ""

@app.route('/')
def starting_page():
    return render_template('index.html', error_message=error_message)

#This info could all be gotten from Mongo
def isValid(email, captain_email):
    global error_message
    global users
    global groups
    username_end = len(email)-12
    username = email[0 : username_end]
    if username in users:
        error_message+="You already have a form on file.  Please contact the Social Club Work Group if you would like to remove your former entry and resubmit"
        return False
    else:
        print(username)
        users.add(username)
    if captain_email != "":
        if captain_email in groups:
            member_list = groups[captain_email]
            if len(member_list)==4:  #This number may change
                error_message+="Sorry.  There are already 4 people in that group"
                return False
        else:
            groups[captain_email] = list()
        groups[captain_email].append(username)
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
