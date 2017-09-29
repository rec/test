from os import listdir
from os.path import isfile, join
path = "/net/u/1/j/jongiles/scripts/domains/names"
test_string1 = "Name server"
test_string2 = "name server"
test_string3 = "Name Server"

active_domains = []
inactive_domains = []

domainfiles = [f for f in listdir(path) if isfile(join(path, f))]
##	print (domainfiles)
for item in domainfiles:
	no_nameserver = 'False'
	print(item)
	fullpath = join(path,item)
	with open(fullpath) as file_object:
		lines = file_object.readlines()
	for line in lines:
		line=line.strip()
		if test_string1 in line: 
			print(line)
			break
		elif test_string2 in line:
                        print(line)
			break
                elif test_string3 in line:
                        print(line)
			break
		else:
			no_nameserver = 'True'

	if no_nameserver == 'True' :
		inactive_domains.append(item)
		
print("This is a list of inactive domains")
print(inactive_domains)
