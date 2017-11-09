def gen1():
    for i in range(3):
        print('gen1', i)
        yield i

def gen2():
    for i in range(4):
        print('gen2', i)
        yield i

print('about to zip')
gen = zip(gen1(), gen2())
print('zipped')
for g1, g2 in gen:
    print('in zip', g1, g2)
