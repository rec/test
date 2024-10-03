def is_anagram(s: str, t: str) -> bool:
    def counter(x):
        r = {}
        for i in x:
            r[i] = r.get(i, 0) + 1
        return r

    return counter(s) == counter(t)

def is_anagram_long(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    character_count_very_long = [0] * 26

    for extremely_long_index in s:
        character_count_very_long[ord(extremely_long_index) - ord('a')] += 1
    for extremely_long_index in t:
        character_count_very_long[ord(extremely_long_index) - ord('a')] -= 1
        if character_count_very_long[ord(extremely_long_index) - ord('a')] < 0:
            return False
    for extremely_long_index in character_count_very_long:
        if extremely_long_index != 0:
            return False
    return True


import timeit

def time(fn):
    return timeit.timeit(lambda: fn('stressed', 'desserts'), number=10000)


print('long names', time(is_anagram_long))
print('short names', time(is_anagram_short))
