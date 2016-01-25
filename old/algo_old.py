#When testing, MUST PUT MORE THAN ONE NAME in group
from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.socialclubs
participants=db.participants
cursor = db.participants.find()

#this may change
NUM_CLUBS=3
#this may also change
#GROUP_CODES = ["28370", "82341", "83242", "93763"]
GROUP_CODES=[]
groups = list() #LIST OF GROUPS
entries = list()
clubs = list()

class Club(object):
        """A class that turns clubs into objects"""
        def __init__(self, grades, genders, ec_dict, ec_list):
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
                if len(entry.names)==1:
                        self.grades[entry.grades[0]]+=1
                        self.genders[entry.genders[0]]+=1
                else:
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
                        self.grades[entry.grades[0]]-=1
                        self.genders[entry.genders[0]]-=1
                else:
                        for i in range (0, 4):
                                self.grades[i]+=entry.grades[i]
                        for j in range(0, 3):
                                self.genders[j]-=entry.genders[j]
                for e in entry.ec_list:
                        self.ec_dict[e]-=entry.ec_dict[e]
                entry.clubIX = -1
                
totals = Club([0,0,0,0], [0,0,0], dict(), list())
constraints = Club([0,0,0,0], [0,0,0], dict(), list())

class Entry(object):
        """A class that turns participants into objects"""
        def __init__(self, _id, names, grades, genders, ec_list, ec_dict, clublist, ix):
                self._id = _id #for groups, this is their group code
                self.names=names
                self.grades=grades
                self.genders=genders
                self.ec_list = ec_list
                self.ec_dict = ec_dict
                self.clublist = clublist
                self.clubIX=ix

        def add_to_group(self, name, grade, gender, stud_ecs, clublist):
                self.names.append(name)
                self.grades[grade]+=1
                self.genders[gender]+=1
                for e in stud_ecs:
                        if e in self.ec_dict:
                                self.ec_dict[e]+=1
                        else:
                                self.ec_dict[e]=1
                                self.ec_list.append(e)
                self.clublist=clublist

def init_groups_and_clubs():
        global groups
        global GROUP_CODES
        for g in GROUP_CODES:
                groups.append(Entry(g, list(), [0,0,0,0], [0,0,0], list(), dict(), list(), -1))
        global NUM_CLUBS
        global clubs
        for j in range (0, NUM_CLUBS):
                clubs.append(Club([0,0,0,0], [0,0,0], dict(), list()))
                
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
        for entry in cursor:
                _id = entry['_id']
                name = entry['name']
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
                group_code = entry['group']
                if(group_code==""):
                        global entries
                        s = Entry(_id, [name], [grade], [gender], ec_list, ec_dict, clublist, -1)
                        entries.append(s)
                else:
                        global groups
                        ix=int(group_code[4])  #Change if group codes change
                        groups[ix].add_to_group(name, grade, gender, ec_list, clublist)
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
        if entry.clubIX!=-1:
                clubs[ix].remove(entry)
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
                
def main ():
        init_groups_and_clubs()
        make_entries()
        append_groups()
        sort(0)
        test()

if __name__ == '__main__':
        main()
