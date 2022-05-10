PREFIX = '/Volumes/McLuhan/Pictures/various iphotos/iPhoto Library - 2'

def dedupe(lines):
    was_hash = False
    line_count = hash_count = 0

    for line in lines:
        if line.strip() and not line.startswith('#'):
            if line[0].isspace():
                if was_hash and not line.strip().startswith(PREFIX):
                    print(line)
                was_hash = False
            else:
                was_hash = True

        line_count += 1
    print(line_count, hash_count)


with open('out.txt') as fp:
    dedupe(fp)
