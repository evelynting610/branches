def read(file):
	clubs = "["
	for aline in file:
                        clubs+="'"
                        clubs+=aline.strip()
                        clubs+="',  "
	return clubs

file=open ("studentclubs.txt", 'r')
club_list=read(file)
file.close()

newfile = open("clublist2.txt", 'w')
newfile.write(club_list)
##for i in range(0, len(club_list)):
##	newfile.write(club_list[i]+', ')
newfile.close()
