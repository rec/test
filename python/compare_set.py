filter_list = [f"{i:03}" for i in range(1000)]
hints = {"291": (1, 1), "245": (1, 0), "463": (2, 0), "578": (0, 0), "569": (1, 0)}

for number, (correct, right_place) in hints.items():
    def position_set(s: str) -> set[str]:
        return {f'{k}{i}' for i, k in enumerate(s)}

    sk, psk = set(number), position_set(number)

    def matches_hint(n: str) -> bool:
        return len(sk & set(n)) == correct and len(psk & position_set(n)) == right_place

    filter_list = [n for n in filter_list if matches_hint(n)]

assert filter_list == ['394'], filter_list
print('ok')
