class Locals:
    def one(self):
        a, b = 'ab'
        print(locals())


Locals().one()
