import itertools


def vignere(message: str, key: str) -> str:
    assert message.isalpha() and key.isalpha()
    message, key = message.lower(), key.lower()

    A = ord('a')
    keys = itertools.cycle([ord(k) - A for k in key])
    messages = (ord(i) - A for i in message)
    return ''.join(chr(A + (k + m) % 26) for k, m in zip(keys, messages))


if __name__ == '__main__':
    import sys
    _, key, *msg = sys.argv
    print(*(vignere(key, m) for m in msg))
