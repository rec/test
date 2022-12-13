class LineOffsets:
    def __len__(self) -> int:
        return 5

    def __getitem__(self, i: int) -> int:
        return 'abcde'[i]



print(list(LineOffsets()))
