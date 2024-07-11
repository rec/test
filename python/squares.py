
count = match = 0

for i in range(10_000, 20_000):
    for j in range(i + 1, 20_000):
        count += 1
        total = (i * i + j * j) ** 0.5
        if int(total) == total:
            match += 1
            # print(i, j)

print('total', count, match, 100 * (match / count))
