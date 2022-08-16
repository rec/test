from dataclasses import dataclass
import typing


@dataclass
class Optional:
    entry: typing.Optional[typing.Any] = None

    def __iter__(self):
        if self.entry:
            yield self.entry


empty = Optional()
full = Optional(1)

for i in empty:
    assert False
else:
    print('empty is empty')

for i in full:
    print('full contains', i)
    break
else:
    assert False
