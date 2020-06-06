i = 0

while i < 3:
    print(i)
    i += 1
    if i == 4:
        print('break')
        break
else:
    print('else!', i)

i = 0

while i < 4:
    print(i)
    i += 1
    if i == 4:
        print('break')
        break
else:
    print('else!', i)
