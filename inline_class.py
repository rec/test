class Foo:
    def __init__(self):
        print('there')

    class Bar(Foo):
        def __init__(self):
            print('here')


Foo.Bar()
