class Foo:
    class Bar:
        def __init__(self):
            print('here')

    def __init__(self):
        print('there')
        self.bar = Bar()


Foo.Bar()
