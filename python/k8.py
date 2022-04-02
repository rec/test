import itertools, string

def count_em():
    letters = set(string.ascii_uppercase)
    numbers = set(string.digits)
    chars = string.ascii_uppercase + string.digits

    for word in itertools.product(*[chars] * 6):
        if 'K' in word and '8' in word and len(numbers.intersection(word)) == 3:
            # A generator is easier to debug
            # because you can just fetch a few elements.
            yield ''.join(word)

for word in count_em():
    print(word)
