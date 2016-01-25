from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants=db.participants
cursor = db.participants.find()

#this may change
#Also FIX club_names once you know club names
NUM_CLUBS=3
groups = list()
entries = list()
clubs = list()

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
                        self.names.append(entry.names)
                        self.emails.append(entry.emails)
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
        for j in range (0, NUM_CLUBS):
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
                constraints.genders[ix]= int(totals.genders[ix]/NUM_CLUBS)+1
        for ix in range(0, 4):
                constraints.grades[ix]= int(totals.grades[ix]/NUM_CLUBS)+1
        ec_list = totals.ec_list
        constraints.ec_list=ec_list
        for ix in range(0, len(ec_list)):
                key = ec_list[ix]
                constraints.ec_dict[key]= int(totals.ec_dict[key]/NUM_CLUBS)+1
                
def make_entries():
        ix=0
        dict_from_capt_to_ix = dict()
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
                if(capt_email==""):
                        global entries
                        s = Entry(_id, [name], [email], [grade], [gender], ec_list, ec_dict, clublist, -1)
                        entries.append(s)
                else:
                        global groups
                        if capt_email not in dict_from_capt_to_ix:
                                groups.append(Entry("", list(), list(), [0,0,0,0], [0,0,0], list(), dict(), list(), -1))
                                dict_from_capt_to_ix[capt_email]=ix
                                ix+=1
                        capt_ix = dict_from_capt_to_ix[capt_email]
                        if email==capt_email:
                                groups[capt_ix].clublist=clublist
                                #the id for a group is the captain's _id
                                groups[capt_ix]._id = _id
                        groups[capt_ix].add_to_group(name, email, grade, gender, ec_list)
                global totals
                totals.calc_totals(grade, gender, ec_list)
        make_constraints_club()


def sort (curr):
        global entries
        global clubs
        if curr==len(entries):
                return True
        entry = entries[curr]
        clublist = entry.clublist
        for ix in clublist:
                if constraints_work(entry, clubs[ix]):
                        clubs[ix].put_in(entry)
                        entry.clubIX=ix
                        if (sort(curr+1)):
                                return True
                        else:
                                clubs[ix].remove(entry)
##        if entry.clubIX!=-1:
##                clubs[ix].remove(entry)
        return False

def constraints_work(entry, club):
        global constraints
        if len(entry.names)==1:
                grade = entry.grades[0]
                gr_const = 1+club.grades[grade]
                if(gr_const > constraints.grades[grade]):
                        return False
                ge = entry.genders[0]
                ge_const = 1+club.genders[ge]
                if(ge_const >constraints.genders[ge]):
                        return False
        else:
                for i in range(0, 4):
                        gr_const = club.grades[i]+entry.grades[i]
                        if(gr_const > constraints.grades[i]):
                                return False
                for j in range(0, 3):
                        ge_const =club.genders[j] + entry.genders[j]
                        if(ge_const >constraints.genders[j]):
                                return False
        for ec in entry.ec_list:
                if ec in club.ec_dict and  entry.ec_dict[ec]+club.ec_dict[ec]>constraints.ec_dict[ec]:
                        return False
        return True

def test():
        global entries
        global clubs
        for entry in entries:
                print entry.names, ":"
                print "\t their clublist was", entry.clublist
                print "\tin club", entry.clubIX
                
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
        club_names = ["Club 0", "Club 1", "Club 2"]
        for ix in range(NUM_CLUBS):
                club=clubs[ix]
                print "In", club_names[ix], ":"
                for i in range(len(club.names)):
                        print "\t", club.names[i], " <", club.emails[i], ">"
                

def b_print_pretty():
        global totals
        print "In the applicant pool, there are:"
        print "\t", totals.grades[0], "people in grade 0,", totals.grades[1], "in grade 1,", totals.grades[2], "in grade 2,", "and", totals.grades[3], "in grade 3;"
        print "\t", totals.genders[0], "people of gender 0,", totals.genders[1], "of gender 1,", "and", totals.genders[2], "of gender 2;"
        for ec in totals.ec_list:
                num_people=totals.ec_dict[ec]
                if num_people==1:
                        print "\t1 person in extra-curricular activity #", ec
                else:
                        print "\t", num_people, "people in extra-curricular activity #", ec
        global entries
        global groups
        groups_length = len(groups)
        students_length = len(entries)-groups_length
        if students_length>0:
                print "Individual Applicants:"
                for ix in range(students_length):
                        entry=entries[ix]
                        print "\t id:", entry._id
                        print "\t\t grade:", entry.grades[0]
                        print "\t\t gender:", entry.genders[0]
                        ec_string ="\t\t extra-curricular activities:"
                        for ec in entry.ec_list:
                                ec_name = str(ec)+", "
                                ec_string+=ec_name
                        print ec_string
        if groups_length>0:
                #group ID is captain's ID
                print "Group Applicants:"
                for ix in range(groups_length):
                        entry=groups[ix]
                        print "\t Group:", entry._id
                        print "\t\t", entry.grades[0], "people in grade 0,", entry.grades[1], "in grade 1,", entry.grades[2], "in grade 2,", "and", entry.grades[3], "in grade 3;"
                        print "\t\t", entry.genders[0], "people of gender 0,", entry.genders[1], "of gender 1,", "and", entry.genders[2], "of gender 2;"
                        for ec in entry.ec_list:
                                num_people=entry.ec_dict[ec]
                                if num_people==1:
                                        print "\t\t1 person in extra-curricular activity #", ec
                                else:
                                        print num_people, "\t\tpeople in extra-curricular activity #", ec
                        
        
def main ():
        init_clubs()
        make_entries()
        append_groups()
        sort(0)
        test()
        a_print_pretty()

if __name__ == '__main__':
        main()
