class StaticSelf:
    def __init__(self):
        class C:
            SELF = self

        self.c = C()
        assert self.c.SELF is self
