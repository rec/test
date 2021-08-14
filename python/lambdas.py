fs = [(lambda: i) for i in range(8)]
print(*(f() for f in fs))
