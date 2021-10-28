import sys
import psutil

SIZE = 100_000_000

#memory in use prior to generating list
prior_used = psutil.virtual_memory().used

print(f"Prior used: {round(prior_used/1e9, 2)} GB")
if True:
    z = list(range(SIZE))
else:
    z = [object() for i in range(SIZE)]

list_size = sys.getsizeof(z)
print(f"List size: {round(list_size/1e9, 2)} GB")

#memory in use after to generating list
post_used = psutil.virtual_memory().used
print(f"Post used: {round(post_used/1e9, 2)} GB")

difference = post_used - prior_used
print(f"Memory used by list: {round(difference/1e9, 2)} GB")

#clear the list
z = None
after_deleting = psutil.virtual_memory().used
print(f"Memory used after clearing the list: {round(after_deleting/1e9, 2)} GB")

# output:
# Prior used: 3.27 GB
# List size: 9.0 GB
# Post used: 43.87 GB
# Memory used by list: 40.6 GB
# Memory used after clearing the list: 3.28 GB
