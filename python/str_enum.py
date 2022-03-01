from enum import Enum, _EnumDict
import xmod


@xmod
def str_enum(classname, *items):
    ed = _EnumDict()
    ed.update({i: i for i in items})
    return type(classname, (str, Enum), ed)
