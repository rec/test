
class Locals:
    def one(self):
        a, b = 'ab'
        print(locals())

        locals().pop('a')
        print(locals())


Locals().one()
