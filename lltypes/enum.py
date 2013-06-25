import ctypes

class EnumNS(type(ctypes.c_uint)):

    def __new__(meta, name, bases, dict):
        if not "_opts_" in dict:
            _opts_ = {}
            for key,value in dict.items():
                if not key.startswith("_"):
                    _opts_[key] = value
            dict["_opts_"] = _opts_

        cls = type(ctypes.c_uint).__new__(meta, name, bases, dict)
        for key,value in cls._members_.items():
            globals()[key] = value
        return cls

class CtypesEnum(ctypes.c_uint):
    __metaclass__ = EnumNS
    _members_ = {}

    def __init__(self, value):
        for k,v in self._members_.items():
            if v == value:
                self.name = k
                break
        else:
            raise ValueError()
        ctypes.c_uint.__init__(self, value)
