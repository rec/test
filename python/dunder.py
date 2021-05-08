class Dunder(str):
    def __repr__(self):
        return 'Dunder'


dunder = Dunder()
dunder.__repr__ = lambda: 'Dover'

print(repr(dunder), dunder.__repr__())

# Prints
#   Dunder Dover
