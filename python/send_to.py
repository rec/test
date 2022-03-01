# https://stackoverflow.com/a/36946209/43839


class Getter:
    data = 1, 2, 3, 4

    def run(self, cb):
        for i in self.data:
            cb(i)


def converter():
    x = None
    while True:
        x = yield x
        print(x)


g = Getter()

c = converter()
c.send(None)
g.run(c.send)
print('closing')
c.close()

for i, x in enumerate(c):
    print(i, x)
    if x is None:
        break
