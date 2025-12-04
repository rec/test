from enum import Enum, auto, StrEnum


class Alpha(str, Enum):
    a = "a"
    bee = "bee"


class Beta(StrEnum):
    a = auto()
    bee = auto()


print(Alpha.a, Alpha.bee, "a" == Alpha.a, "bee" == Alpha.bee)
print(Beta.a, Beta.bee, "a" == Beta.a, "bee" == Beta.bee)
