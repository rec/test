hints = {"291": (1, 1), "245": (1, 0), "463": (2, 0), "578": (0, 0), "569": (1, 0)}
filter_list = []

for i in range(1000):
    n = f'{i:03}'
    if all(
        len(set(number) & set(n)) == correct
        and sum(i == j for i, j in zip(number, n)) == right_place
        for number, (correct, right_place) in hints.items()
    ):
        filter_list.append(n)


assert filter_list == ['394'], filter_list
print('ok')
