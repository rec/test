import yaml

for i in range(127):
    if chr(i).isalnum():
        continue
    word = chr(i) + 'test'
    try:
        if yaml.load(word) != word:
            continue
    except:
        continue
    print(chr(i), end='')

print()
