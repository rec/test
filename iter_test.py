class Iter:
    def __getitem__(self, i):
        if i >= 5:
            raise IndexError
        return i

    def __len__(self):
        return 5
