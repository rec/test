class ClassWithStr(type):
  def __new__(cls, name, bases, dict):
    def __str__(self):
      attributes = ', '.join([f'{k}={v}' for k,v in self.__dict__.items()])
      return f'{self.__class__.__name__}({attributes})'

    dict['__str__'] = __str__
    return super().__new__(cls, name, bases, dict)



def with_str(cls):
    def __str__(self):
        attributes = ', '.join([f'{k}={v}' for k,v in self.__dict__.items()])
        return f'{self.__class__.__name__}({attributes})'

    cls.__str__ = __str__
    return cls


class Dog1(metaclass=ClassWithStr):
  def __init__(self, name, age):
    self.name = name
    self.age = age


@with_str
class Dog2:
  def __init__(self, name, age):
    self.name = name
    self.age = age


print(Dog1('Oliver', 11), Dog2('Mia', 18))
