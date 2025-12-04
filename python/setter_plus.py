class C:
    @property
    def x(self):
        return getattr(self, "_x", 0)

    @x.setter
    def x(self, x):
        self._x = x

    def __str__(self):
        return str(self.x)


print(c := C())
c.x += 1
print(c)
