__all__ = 'bang', 'Bang'

bang = 'bang!'
print('!!!!', __package__)
print('!!!!', __name__)
print('!!!!', __file__)

class Bang:
    pass

print(locals().keys())
