
def read(file):
	clubs = list()
	count=0
	for aline in file:
		option = "<option value="+str(count)+">"+aline+"</option>"
		clubs.append(option)
		count+=1
	return clubs

file=open ("studentclubs.txt", 'r')
club_list=read(file)
file.close()

newfile = open("clublist.txt", 'w')
for i in range(0, len(club_list)):
	newfile.write(club_list[i]+'\n')
newfile.close()