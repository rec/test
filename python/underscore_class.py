class A:
    def one(self):
        print('one', __class__, self.__class__)

    @classmethod
    def two(cls):
        print('two', __class__, cls)

    @staticmethod
    def three():
        print('three', __class__)


class B(A):
    pass


A().one()
A().two()
A().three()
B().one()
B().two()
B().three()
