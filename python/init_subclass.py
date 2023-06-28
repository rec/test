class Philosopher:
    def __init_subclass__(cls, /, default_name='Bertrand', **kwargs):
        print('!!!', cls)
        super().__init_subclass__(**kwargs)
        cls.default_name = default_name


class AustralianPhilosopher(Philosopher, default_name="Bruce"):
    pass


class FrenchPhilosopher(AustralianPhilosopher):
    pass


print('australia')
print(AustralianPhilosopher().default_name)

print('france')
print(FrenchPhilosopher().default_name)
