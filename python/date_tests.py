from datetime import datetime
import time


# Get a UTC timestamp:

print(datetime.now().isoformat())

# Convert a timestamp to a datetime

timestamp = time.time()
# dt = datetime.utcfromtimestamp(timestamp, tz=None)
dt = datetime.fromtimestamp(timestamp, tz=None)
print(dt)


# Replace fields in a datetime:

print(dt.replace(year=2001))


# print a string

fmt = '%Y/%m/%d:%H:%M:%S'
d = dt.strftime(fmt)
print(d)

# Parse a string
print(datetime.strptime(d, fmt))
