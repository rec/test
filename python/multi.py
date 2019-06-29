class Multi(object):
    ITEMS = (1, 3), (5, 8)

    def __getitem__(self, i):
        return self.ITEMS[i[0]][i[1]]

    def __setitem__(self, i, x):
        self.ITEMS[i[0]][i[1]] = x

    def __len__(self):
        return 2, 2
