def solve(path):
    file = open(path, "r")
    lines = file.readlines()
    count = 0
    for row in lines:
        if row.rstrip() and not row.startswith("#"):
            count +=1
    return count


print(solve('python/op2.txt'))
