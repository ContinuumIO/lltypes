import ctypes

# Python 2/3 compat
def with_metaclass(meta, base=object):
    return meta("NewBase", (base,), {'_members_': {}})

SimpleData = type(ctypes.c_uint)

class EnumNS(SimpleData):

    def __new__(meta, name, bases, dict):
        if not "_opts_" in dict:
            _opts_ = {}
            for key,value in list(dict.items()):
                if not key.startswith("_"):
                    _opts_[key] = value
            dict["_opts_"] = _opts_

        cls = type(ctypes.c_uint).__new__(meta, name, bases, dict)
        for key,value in list(cls._members_.items()):
            globals()[key] = value
        return cls

class CtypesEnum(with_metaclass(EnumNS, ctypes.c_uint)):

    def __init__(self, value):
        for k,v in list(self._members_.items()):
            if v == value:
                self.name = k
                break
        else:
            raise ValueError()
        ctypes.c_uint.__init__(self, value)
