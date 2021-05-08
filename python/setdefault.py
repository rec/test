letters = {}
for ch in 'abcdefghij':
    letters.setdefault(ord(ch) % 3, []).append(ch)

print(letters)
