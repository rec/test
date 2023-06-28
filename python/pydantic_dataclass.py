from typing import Literal, Union
from pydantic import BaseModel, Field, ValidationError


class Dog(BaseModel):  # Correct
    pet_type: Literal['dog'] = 'dog'
    barks: float


class Cat(BaseModel):
    meows: int
    pet_type: Literal['cat'] = Literal['cat']  # This doesn't JSONize right


class Lizard(BaseModel):
    pet_type: Literal['reptile', 'lizard']  # This is a required parameter! :-/
    scales: bool = True


class Model(BaseModel):
    pet: Union[Cat, Dog, Lizard] = Field(..., discriminator='pet_type')
    n: int


print(Model(pet={'pet_type': 'dog', 'barks': 3.14}, n=1))
#> pet=Dog(pet_type='dog', barks=3.14) n=1
try:
    Model(pet={'pet_type': 'dog'}, n=1)
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    pet.dog.barks
      Field required [type=missing, input_value={'pet_type': 'dog'}, input_type=dict]
    """

try:
    Model(pet={'pet_type': 'frog', 'barks': 3.0})
except ValidationError as e:
    print(e)

print(cat := Cat(meows=10).dict())
print(dog := Dog(barks=3.2).dict())

import json
print(json.dumps(dog, indent=2))
try:
    print(json.dumps(cat, indent=2))  # Raises an exception
except TypeError:
    print('oops')

# Subclassing

class Chow(BaseModel):
    pet_type: Literal['chow'] = 'chow'


class Model2(BaseModel):
    pet: Union[Cat, Dog, Lizard, Chow] = Field(..., discriminator='pet_type')
    n: int


print(Model2(pet={'pet_type': 'dog', 'barks': 3.14}, n=1))
print(Model2(pet={'pet_type': 'chow', 'barks': 0}, n=1))
