def make_class(do_it):
    if not do_it:
        return

    class Foo(do_it):
        pass

    return Foo
