import sys, csv

WRITE = True
fieldnames = 'one', 'two', 'three'

if WRITE:
    # quoting = csv.QUOTE_ALL
    # quoting = csv.QUOTE_NONNUMERIC
    quoting = csv.QUOTE_MINIMAL
    w = csv.DictWriter(sys.stdout, fieldnames, quoting=quoting)
    w.writeheader()
    w.writerow({'one': None, 'two': 'None', 'three': ''})

else:
    with open(sys.argv[1], 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            print(row)
