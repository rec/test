hashes = set(i.strip() for i in open('hashes.txt'))
archives = (i.strip() for i in open('archive.txt'))
asuffix = (a.split('.')[0] for a in archives)
ahash = {a.split('_')[-1] for a in asuffix}
print(len(hashes), len(ahash))
print(hashes - ahash)
