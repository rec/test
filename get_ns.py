from os import listdir
from os.path import isfile, join

path = "/net/u/1/j/jongiles/scripts/domains/names"

TEST_STRINGS = "Name server", "name server", "Name Server"

active_domains = []
inactive_domains = []

domainfiles = [f for f in listdir(path) if isfile(join(path, f))]
##    print (domainfiles)

for item in domainfiles:
    print(item)

    fullpath = join(path,item)

    with open(fullpath) as file_object:
        lines = file_object.readlines()

    if not any(any(ts in line for ts in TEST_STRINGS) for line in lines):
        inactive_domains.append(item)

print("This is a list of inactive domains")
print(inactive_domains)
