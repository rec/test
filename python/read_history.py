from collections import Counter

counter = Counter()
for line in open('/tmp/history.txt'):
    command = line.split()[1]
    counter[command] += 1
    print(command)

print(counter)
