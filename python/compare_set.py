def positional_set(value):
    return {f'{k}{i}' for i, k in enumerate(value)}

filter_list = [f"{i:03}" for i in range(1000)]
hints = {"291": (1, 1), "245": (1, 0), "463": (2, 0), "578": (0, 0), "569": (1, 0)}
for (k, v) in hints.items():
    sk = set(k)
    psk = positional_set(k)

    filter_list = [
        hint for hint in filter_list
        if len(sk & set(hint)) == v[0] and
        len(psk & positional_set(hint)) == v[1]
]

assert filter_list == ['394'], filter_list
print('ok')
