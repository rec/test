class Get(object):
    def __getitem__(self, i):
        return i

    def __setitem__(self, i, x):
        print('set', i, x)
