

class Missing(dict):
    def __missing__(self, key: str) -> str:
        return key + '-oops'


m = Missing()

print(m['KEY'])
print(m.keys())
