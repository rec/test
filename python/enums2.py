import enum

class Serializer(enum.Enum):
    dill = 'dill'
    pickle = 'pickle'

    @property
    def wombat(self):
        return self.value + '-wombat'


print(Serializer.dill.wombat)
