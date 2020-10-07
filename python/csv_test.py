import sys, csv

csv_file = open(sys.argv[1], 'r')
csv_reader = csv.DictReader(csv_file)

for row in csv_reader:
    print(row)
