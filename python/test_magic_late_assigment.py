class Test:
    pass

Test.__str__ = lambda self: 'suprise'
print(Test())
