class Patchee:
    pass


print(Patchee())
Patchee.__str__ = lambda a: 'patched'
print(Patchee())
