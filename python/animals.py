animals = {1: 'python'}
loops = 1
for key in animals:
    del animals[key]
    animals[key + 1] = None
    print(loops)
    loops += 1
