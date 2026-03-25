filter_list = [f"{i:03}" for i in range(1000)]
hints = {"291": (1, 1), "245": (1, 0), "463": (2, 0), "578": (0, 0), "569": (1, 0)}

for number, (correct, right_place) in hints.items():
    def matches_hint(n: str) -> bool:
        return (
            len(set(number) & set(n)) == correct
            and sum(i == j for i, j in zip(number, n)) == right_place
        )

    filter_list = [n for n in filter_list if matches_hint(n)]

assert filter_list == ['394'], filter_list
print('ok')
