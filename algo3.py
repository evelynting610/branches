from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants=db.participants

#Change club names
#this may change
NUM_CLUBS=6
club_names = ["first", "second", "third", "fourth", "fifth", "sixth"]
groups = list()
entries = list()
clubs = list()
email_to_clublist = dict()

class Club(object):
        """A class that turns clubs into objects"""
        def __init__(self, names, emails, grades, genders, ec_dict, ec_list):
                self.names = names
                self.emails=emails
                self.grades=grades
                self.genders=genders
                self.ec_dict=ec_dict
                self.ec_list=ec_list
        def calc_totals(self, grade, gender, ec_list):
                self.grades[grade]+=1
                self.genders[gender]+=1
                for e in ec_list:
                        if e in self.ec_dict:
                                self.ec_dict[e]+=1
                        else:
                                self.ec_dict[e]=1
                                self.ec_list.append(e)
        def put_in(self, entry):
                name_length = len(entry.names)
                if name_length==1:
                        self.names.append(entry.names[0])
                        self.emails.append(entry.emails[0])
                        self.grades[entry.grades[0]]+=1
                        self.genders[entry.genders[0]]+=1
                else:
                        self.names.append("group")
                        self.emails.append(name_length)
                        for ix in range(name_length):
                                self.names.append(entry.names[ix])
                                self.emails.append(entry.emails[ix])
                        for i in range (0, 4):
                                self.grades[i]+=entry.grades[i]
                        for j in range(0, 3):
                                self.genders[j]+=entry.genders[j]
                for e in entry.ec_list:
                        if e in self.ec_dict:
                                self.ec_dict[e]+=entry.ec_dict[e]
                        else:
                                self.ec_dict[e]=entry.ec_dict[e]
                                self.ec_list.append(e)

        def remove(self, entry):
                if len(entry.names)==1:
                        self.names.pop()
                        self.emails.pop()
                        self.grades[entry.grades[0]]-=1
                        self.genders[entry.genders[0]]-=1
                else:
                        for name in entry.names:
                                self.names.pop()
                                self.emails.pop()
                        self.names.pop()   #removing word "group"
                        self.emails.pop()
                        for i in range (0, 4):
                                self.grades[i]-=entry.grades[i]
                        for j in range(0, 3):
                                self.genders[j]-=entry.genders[j]

                for e in entry.ec_list:
                        self.ec_dict[e]-=entry.ec_dict[e]
                entry.clubIX = -1

totals = Club(list(), list(), [0,0,0,0], [0,0,0], dict(), list())
constraints = Club(list(), list(), [0,0,0,0], [0,0,0], dict(), list())

class Entry(object):
        """A class that turns participants into objects"""
        def __init__(self, _id, names, emails, grades, genders, ec_list, ec_dict, clublist, ix):
                self._id = _id
                self.names=names
                self.emails=emails
                self.grades=grades
                self.genders=genders
                self.ec_list = ec_list
                self.ec_dict = ec_dict
                self.clublist = clublist
                self.clubIX=ix

        def add_to_group(self, name, email, grade, gender, stud_ecs):
                self.names.append(name)
                self.emails.append(email)
                self.grades[grade]+=1
                self.genders[gender]+=1
                for e in stud_ecs:
                        if e in self.ec_dict:
                                self.ec_dict[e]+=1
                        else:
                                self.ec_dict[e]=1
                                self.ec_list.append(e)

def init_clubs():
        global NUM_CLUBS
        global clubs
        for j in range (NUM_CLUBS):
                clubs.append(Club(list(), list(), [0,0,0,0], [0,0,0], dict(), list()))

def append_groups():
        global groups
        global entries
        for group in groups:
                entries.append(group)


def make_constraints_club():
        global constraints
        global NUM_CLUBS
        for ix in range(0, 3):
                constraints.genders[ix]= int(totals.genders[ix]/NUM_CLUBS)+2
        for ix in range(0, 4):
                constraints.grades[ix]= int(totals.grades[ix]/NUM_CLUBS)+3
        ec_list = totals.ec_list
        constraints.ec_list=ec_list
        for ix in range(0, len(ec_list)):
                key = ec_list[ix]
                constraints.ec_dict[key]= int(totals.ec_dict[key]/NUM_CLUBS)+3

dict_from_capt_to_ix = dict()
index=0
def make_entries(cursor):
        global index
        global email_to_clublist
        for entry in cursor:
                _id = entry['_id']
                name = entry['name']
                email = entry['email']
                grade = int(entry['grade'])
                gender = int(entry['gender'])
                ec_list = list()
                ec_dict = dict()
                ec1 = int(entry['ec1'])
                ec2 = int(entry['ec2'])
                if ec1!=-1:
                        ec_list.append(ec1)
                        ec_dict[ec1]=1
                if ec2!=-1:
                        ec_list.append(ec2)
                        ec_dict[ec2]=1
                clublist = entry['ranked_clubs']
                capt_email = entry['group']
                email_to_clublist[email] = clublist
                if(capt_email==""):
                        global entries
                        s = Entry(_id, [name], [email], [grade], [gender], ec_list, ec_dict, clublist, -1)
                        entries.append(s)
                else:
                        global groups
                        global dict_from_capt_to_ix
                        if capt_email not in dict_from_capt_to_ix:
                                groups.append(Entry("", list(), list(), [0,0,0,0], [0,0,0], list(), dict(), list(), -1))
                                dict_from_capt_to_ix[capt_email]=index
                                index+=1
                        capt_ix = dict_from_capt_to_ix[capt_email]
                        if email==capt_email:
                                groups[capt_ix].clublist=clublist
                                #the id for a group is the captain's _id
                                groups[capt_ix]._id = _id
                        groups[capt_ix].add_to_group(name, email, grade, gender, ec_list)
                global totals
                totals.calc_totals(grade, gender, ec_list)


def sort (curr):
        global entries
        global clubs
        if curr==len(entries):
                return True
        entry = entries[curr]
        clublist = entry.clublist
        for ix in clublist:
                ix = int(ix)
                if constraints_work(entry, clubs[ix]):
                        clubs[ix].put_in(entry)
                        #print "club ", ix, " added ", entry.emails
                        entry.clubIX=ix
                        if (sort(curr+1)):
                                return True
                        else:
                                clubs[ix].remove(entry)
                                #print "removed ", entry.emails, "\n"
        return False

def constraints_work(entry, club):
        global clubs
        global constraints
        if len(entry.names)==1:
                grade = entry.grades[0]
                gr_const = 1+club.grades[grade]
                if gr_const > constraints.grades[grade]:
                        return False
                ge = entry.genders[0]
                ge_const = 1+club.genders[ge]
                if ge_const >constraints.genders[ge]:
                        return False
        else:
                for i in range(0, 4):
                        gr_const = club.grades[i]+entry.grades[i]
                        if gr_const > constraints.grades[i]:
                                #print "gr const is ", gr_const, "constraint is ", constraints.grades[i]
                                return False
                for j in range(0, 3):
                        ge_const =club.genders[j] + entry.genders[j]
                        if ge_const >constraints.genders[j]:
                                return False
        for ec in entry.ec_list:
                if ec in club.ec_dict and  entry.ec_dict[ec]+club.ec_dict[ec]>constraints.ec_dict[ec]:
                        return False
        return True

def test():
        global entries
        global clubs
        for entry in entries:
                print (entry.emails, ":")
                #IF CLUB LIST IS BLANK, the captain didn't spell his email correctly
                print ("\t their clublist was", entry.clublist)
                print ("\tin club", entry.clubIX)

def is_there_a_solution():
        global constraints
        global groups
        print("grade constraints are ", constraints.grades)
        for g in groups:
                print(g.grades)
        print("gender constraints are ", constraints.genders)
        for g in groups:
                print(g.genders)

def a_print_pretty():
        global clubs
        global email_to_clublist
        global club_names
        results = open("secondround_results.txt", 'w')
        for ix in range(NUM_CLUBS):
                num_first_choice=0
                num_members=0
                club=clubs[ix]
                club_header = "In "+club_names[ix]+" :\n"
                results.write(club_header)
                for i in range(len(club.names)):
                        if club.names[i]!="group":
                                num_members+=1
                                email = club.emails[i]
                                clublist = email_to_clublist[email]
                                if clublist[0]==ix:
                                        num_first_choice+=1
                                member = "\t"+club.names[i]+" <"+email+">\n"
                                results.write(member)
                first_choice = str(num_first_choice)+" out of "+str(num_members)+" marked this as their first choice\n"
                results.write(first_choice)
                gender = "Gender: "+str(club.genders[0])+" women and "+str(club.genders[2])+" men.\n"
                results.write(gender)
                grade = "Grade:  2016= "+str(club.grades[1])+",  2017= "+str(club.grades[0])+",  2018= "+str(club.grades[3])+",  2019= "+str(club.grades[2])+"\n\n\n"
                results.write(grade)
        results.close()


def b_print_pretty():
        global totals
        print ("In the applicant pool, there are:")
        print ("\t", totals.grades[0], "people in grade 0,", totals.grades[1], "in grade 1,", totals.grades[2], "in grade 2,", "and", totals.grades[3], "in grade 3;")
        print ("\t", totals.genders[0], "people of gender 0,", totals.genders[1], "of gender 1,", "and", totals.genders[2], "of gender 2;")
        for ec in totals.ec_list:
                num_people=totals.ec_dict[ec]
                if num_people==1:
                        print ("\t1 person in extra-curricular activity #", ec)
                else:
                        print ("\t", num_people, "people in extra-curricular activity #", ec)
        global entries
        global groups
        groups_length = len(groups)
        students_length = len(entries)-groups_length
        if students_length>0:
                print ("Individual Applicants:")
                for ix in range(students_length):
                        entry=entries[ix]
                        print ("\t id:", entry._id)
                        print ("Ranked Branches:", entry.clublist)
                        print ("\t\t grade:", entry.grades[0])
                        print ("\t\t gender:", entry.genders[0])
                        ec_string ="\t\t extra-curricular activities:"
                        for ec in entry.ec_list:
                                ec_name = str(ec)+", "
                                ec_string+=ec_name
                        print (ec_string)
        if groups_length>0:
                #group ID is captain's ID
                print ("Group Applicants:")
                for ix in range(groups_length):
                        entry=groups[ix]
                        print ("\t Group:", entry._id)
                        print ("\t\tRanked Branches:", entry.clublist)
                        print ("\t\t", entry.grades[0], "people in grade 0,", entry.grades[1], "in grade 1,", entry.grades[2], "in grade 2,", "and", entry.grades[3], "in grade 3;")
                        print ("\t\t", entry.genders[0], "people of gender 0,", entry.genders[1], "of gender 1,", "and", entry.genders[2], "of gender 2;")
                        for ec in entry.ec_list:
                                num_people=entry.ec_dict[ec]
                                if num_people==1:
                                        print ("\t\t1 person in extra-curricular activity #", ec)
                                else:
                                        print (num_people, "\t\tpeople in extra-curricular activity #", ec)


def main ():
        init_clubs()
        make_entries(participants.find())
        make_constraints_club()
        append_groups()
        sort(0)
        test()
        a_print_pretty()

if __name__ == '__main__':
        main()
