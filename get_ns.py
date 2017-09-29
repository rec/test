from os import listdir
from os.path import isfile, join

path = "/net/u/1/j/jongiles/scripts/domains/names"

TEST_STRINGS = "Name server", "name server", "Name Server"

active_domains = []
inactive_domains = []

def is_active_line(line):
    """Return true if the line of the file indicates that the domain is active.
    """
    return any(ts in line for ts in TEST_STRINGS)


def is_active_file(path, item):
    fp = open(join(path, item))
    return any(is_active_file(line) for line in fp)


domainfiles = [f for f in listdir(path) if isfile(join(path, f))]
for item in domainfiles:
    print(item)

    if not if_active_file(path, item):
        inactive_domains.append(item)

print("This is a list of inactive domains")
print(inactive_domains)
