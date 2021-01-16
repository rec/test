def h(i):
    return hex(i)[2:]


r = range(16)

print("   ", *(h(i) for i in r), sep="")
print("   ", *("-" for i in r), sep="")

for i in r:
    print(h(i) + ": ", end="")
    for j in r:
        c = chr(16 * i + j)

        print(c if c.isprintable() else " ", end="")
    print()
