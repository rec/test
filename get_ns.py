import os

path = "/net/u/1/j/jongiles/scripts/domains/names"

TEST_STRINGS = "Name server", "name server", "Name Server"
active_domains = []

def is_active_line(line):
    """Return true if the line of the file indicates that the domain is active.
    """
    return any(ts in line for ts in TEST_STRINGS)


def is_active_domain(f):
    return any(is_active_file(line) for line in open(f))


directory = [os.path.join(path, f) for f in os.listdir(path)]
domainfiles = [f for f in directory if os.path.isfile(f)]
inactive_domains = [f for f in domainfiles if not is_active_domain(f)]

print("This is a list of inactive domains")
print(inactive_domains)
