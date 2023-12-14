from dataclasses import make_dataclass, dataclass

Data = make_dataclass('Data', [('name', str)])

d = Data('Tom')
print(d.name)
