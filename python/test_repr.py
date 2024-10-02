class A:
    def __str__(self):
        return 'A'


class B:
    def __repr__(self):
        return 'B'


print('. str repr')
print(A(), str(A()), repr(A()))
print(B(), str(B()), repr(B()))
