import itertools, string

LETTERS = string.ascii_uppercase
NUMBERS = string.digits
CHARS = string.ascii_uppercase + string.digits


def _next_chars(word):
    if len(word) == 6:
        return ''

    letter_count = sum(i in LETTERS for i in word)
    if letter_count == 3:
        letters = ''
    elif letter_count == 2 and 'K' not in word:
        letters = 'K'
    else:
        letters = LETTERS

    number_count = sum(i in NUMBERS for i in word)
    if number_count == 3:
        numbers = ''
    elif number_count == 2 and '8' not in word:
        numbers = '8'
    else:
        numbers = NUMBERS

    return letters + numbers


def count_em(word=None):
    word = word or []
    nc = _next_chars(word)
    if not nc:
        yield ''.join(word)
    else:
        for c in nc:
            word.append(c)
            yield from count_em(word)
            word.pop()

for word in count_em():
    print(word)
