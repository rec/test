from enum import Enum, auto


class Alpha(str, Enum):
    a = "a"
    bee = "bee"


print(Alpha.a, Alpha.bee, "a" == Alpha.a, "bee" == Alpha.bee)
