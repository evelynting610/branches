from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants=db.participants2

NUM_CLUBS=4
entries = []
groups = []

class Entry(object):
        """A class that turns participants into objects"""
        def __init__(self, names, emails, grades, genders, ec_list, clublist, ix):
                self.names=names
                self.emails=emails
                self.grades=grades
                self.genders=genders
                self.ec_list = ec_list
                self.clublist = clublist
                self.clubIX=ix
        def add_to_group(self, name, email, grade, gender, ec_list):
                self.names.append(name)
                self.emails.append(email)
                self.grades.append(grade)
                self.genders.append(gender)
                for e in ec_list:
                        self.ec_list.append(e)
                
def read_database(cursor):
    dict_from_capt_to_ix = dict()
    index=0
    for entry in cursor:
                name = entry['name']
                email = entry['email']
                grade = entry['grade']
                gender = entry['gender']
                ec_list = list()
                ec1 = int(entry['ec1'])
                ec2 = int(entry['ec2'])
                if ec1!=-1:
                        ec_list.append(ec1)
                if ec2!=-1:
                        ec_list.append(ec2)
                clublist = entry['ranked_clubs']
                capt_email = entry['group']
                if(capt_email==""):
                        global entries
                        s = Entry([name], [email], [grade], [gender], ec_list, clublist, -1)
                        entries.append(s)
                else:
                        global groups
                        if capt_email not in dict_from_capt_to_ix:
                                groups.append(Entry(list(), list(), list(), list(), list(), list(), -1))
                                dict_from_capt_to_ix[capt_email]=index
                                index+=1
                        capt_ix = dict_from_capt_to_ix[capt_email]
                        if email==capt_email:
                                groups[capt_ix].clublist=clublist
                        groups[capt_ix].add_to_group(name, email, grade, gender, ec_list)

def write_database(clubname, ecname):
        global entries
        global groups
        results = open("second_round.txt", 'w')
        results.write("Individuals\n\n")
        for indiv in entries:
                rankedclubs = "\tRanked Clubs: "
                for i in range(0, NUM_CLUBS):
                        rankedclubs+=clubname[indiv.clublist[i]]+", "
                rankedclubs+=clubname[indiv.clublist[NUM_CLUBS]]
                results.write("Name: "+indiv.names[0]+"  <"+indiv.emails[0]+">\n")
                results.write(rankedclubs+"\n")
                ecs = ",  EC's: "
                ec_length = len(indiv.ec_list)-1
                for e in range(0, ec_length):
                        ecs+=ecname[indiv.ec_list[e]]+", "
                if ec_length>-1:
                        ecs+=ecname[indiv.ec_list[ec_length]]
                else:
                        ecs+="None"
                results.write("\tGender: "+indiv.genders[0]+", Grade: "+indiv.grades[0]+ecs+"\n\n")
                
        results.write("Groups\n\n")
        for group in groups:
                names = "Names: "
                namelength = len(group.names)-1
                for n in range(0, namelength):
                        names+=group.names[n]+"<"+group.emails[n]+">, "
                names+=group.names[namelength]+"<"+group.emails[namelength]+">\n"
                results.write(names)

                rankedclubs = "\tRanked Clubs: "
                for i in range(0, NUM_CLUBS):
                        rankedclubs+=clubname[group.clublist[i]]+", "
                rankedclubs+=clubname[group.clublist[NUM_CLUBS]]
                results.write(rankedclubs+"\n")

                genders = "\tGenders:"
                for ge in range(0, namelength):
                        genders+=group.genders[ge]+", "
                genders+=group.genders[namelength]+"\n"
                results.write(genders)

                grades = "\tGrades:"
                for g in range(0, namelength):
                        grades+=group.grades[g]+", "
                grades+=group.grades[namelength]+"\n"
                results.write(grades)

                ecs = "\tEC's: "
                ec_length = len(group.ec_list)-1
                for e in range(0, ec_length):
                        ecs+=ecname[group.ec_list[e]]+", "
                if ec_length>-1:
                        ecs+=ecname[group.ec_list[ec_length]]
                else:
                        ecs+="None"
                results.write(ecs+"\n\n")
                
        results.close()

def read(file):
        clubs = list()
        for aline in file:
                clubs.append(aline.strip())
        return clubs

def main():
        clubname = ["301", "Ailurus", "Buena Vista", "Fourth Wall", "SOS"]
        file=open ("studentclubs.txt", 'r')
        ecname=read(file)
        file.close()
        read_database(participants.find())
        write_database(clubname, ecname)

main()
