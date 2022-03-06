from dataclasses import dataclass


@dataclass
class Data:
    one: str = 'one'
    two: str = 'two'
    three: int = 3

    from dataclasses import asdict, astuple, fields, replace
    fields = classmethod(fields)


print(Data().asdict())
print(Data().astuple())
print(Data().replace(one='ten', three=16))
print(*(f.name for f in Data().fields()))

# If you comment out the `classmethod` line, this line won't work.
print(*(f.name for f in Data.fields()))
