import numpy
import ctypes
import llvm.core as lc
import numbers
import warnings

from . import codes
from . import enum

ptrsize = ctypes.sizeof(ctypes.c_void_p)

#------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------

class NoLlvmMapping(Exception):
    pass
class NoCtypeMapping(Exception):
    pass
class NoDtypeMapping(Exception):
    pass

#------------------------------------------------------------------------
# Types
#------------------------------------------------------------------------

class Type(object):

    def to_dtype(self):
        raise NoDtypeMapping(self)

    def to_llvm(self):
        raise NoLlvmMapping(self)

    def to_ctypes(self):
        raise NoCtypeMapping(self)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)

class Struct(Type):
    def __init__(self, name, *fields):
        self.name = name
        self.fields = fields

    def to_dtype(self):
        fields = [
            (field.name, field.to_dtype())
            for field in self.fields
        ]
        return numpy.dtype(fields)

    def to_llvm(self):
        fields = [
            field.to_llvm()
            for field in self.fields
        ]
        return lc.Type.struct(
            fields,
            self.name
        )

    def to_ctypes(self):
        class struct(ctypes.Structure):
            _fields_ = [
                (field.name, field.to_ctypes())
                for field in self.fields
            ]
        struct.__name__ = self.name
        return struct

class Field(Type):
    def __init__(self, name, endianness, format):
        self.name = name
        self.endianness = endianness
        self.format = format

    def to_dtype(self):
        return numpy.dtype(self.endianness + self.format)

    def to_llvm(self):
        #if self.format.isupper():
            #warnings.warn("Conversion to LLVM may not preserve precision")
        return codes.format_llvm[self.format]

    def to_ctypes(self):
        return codes.format_ctypes[self.format]

class Enum(Type):
    def __init__(self, name, **opts):
        self.name = name
        self.idx = UNInt8(name)
        self.opts = opts

    def to_dtype(self):
        raise NoDtypeMapping(self)

    def to_llvm(self):
        return lc.Type.int(8)

    def to_ctypes(self):
        return type(self.name, (enum.CtypesEnum,), self.opts)

class Union(Type):

    def __init__(self, name, tag, options):
        self.name = name
        self.tag = tag
        self.options = options

    def to_dtype(self):
        raise NoDtypeMapping(self)

    def to_llvm(self):
        fields = [
            field.to_llvm()
            for field in self.fields
        ]
        return lc.Type.struct(
            fields,
            self.name
        )

    def to_ctypes(self):
        class struct(ctypes.Union):
            _fields_ = [
                (field.name, field.to_ctypes())
                for field in self.fields
            ]
        struct.__name__ = self.name
        return struct

class Vector(Type):

    def __init__(self, width, ty):
        if not isinstance(width, numbers.Integral):
            raise ValueError('Must be integral width')
        assert width in [2, 4, 8]

        self.width = width
        self.ty = ty

    def to_dtype(self):
        raise NoDtypeMapping(self)

    def to_ctypes(self):
        raise NoCtypeMapping()

    def to_llvm(self):
        return lc.Type.vector(self.ty.to_llvm(), self.width)

class Pointer(Type):

    def __init__(self, ty):
        self.ty = ty

    @property
    def name(self):
        return self.ty.name

    def to_dtype(self):
        if self.ty.format in ['s', 'c', 'B', 'b']:
            return self.ty.to_dtype()
        else:
            raise NoDtypeMapping()

    def to_ctypes(self):
        return ctypes.POINTER(self.ty.to_ctypes())

    def to_llvm(self):
        return lc.Type.pointer(self.ty.to_llvm())

#------------------------------------------------------------------------
# Big Endian
#------------------------------------------------------------------------

def UBInt8(name):
    return Field(name, ">", "B")
def UBInt16(name):
    return Field(name, ">", "H")
def UBInt32(name):
    return Field(name, ">", "L")
def UBInt64(name):
    return Field(name, ">", "Q")

def SBInt8(name):
    return Field(name, ">", "b")
def SBInt16(name):
    return Field(name, ">", "h")
def SBInt32(name):
    return Field(name, ">", "l")
def SBInt64(name):
    return Field(name, ">", "q")

#------------------------------------------------------------------------
# Little Endian Integers
#------------------------------------------------------------------------

def ULInt8(name):
    return Field(name, "<", "B")
def ULInt16(name):
    return Field(name, "<", "H")
def ULInt32(name):
    return Field(name, "<", "L")
def ULInt64(name):
    return Field(name, "<", "Q")

def SLInt8(name):
    return Field(name, "<", "b")
def SLInt16(name):
    return Field(name, "<", "h")
def SLInt32(name):
    return Field(name, "<", "l")
def SLInt64(name):
    return Field(name, "<", "q")

#------------------------------------------------------------------------
# Native Endian Integers
#------------------------------------------------------------------------

def UNInt8(name):
    return Field(name, "=", "B")
def UNInt16(name):
    return Field(name, "=", "H")
def UNInt32(name):
    return Field(name, "=", "L")
def UNInt64(name):
    return Field(name, "=", "Q")

def SNInt8(name):
    return Field(name, "=", "b")
def SNInt16(name):
    return Field(name, "=", "h")
def SNInt32(name):
    return Field(name, "=", "l")
def SNInt64(name):
    return Field(name, "=", "q")

#------------------------------------------------------------------------
# IEEE Floating Point
#------------------------------------------------------------------------

def BFloat32(name):
    return Field(name, ">", "f")
def LFloat32(name):
    return Field(name, "<", "f")
def NFloat32(name):
    return Field(name, "=", "f")

def BFloat64(name):
    return Field(name, ">", "d")
def LFloat64(name):
    return Field(name, "<", "d")
def NFloat64(name):
    return Field(name, "=", "d")

def Bool(name):
    return Field(name, "=", "?")

#------------------------------------------------------------------------
# Defaults
#------------------------------------------------------------------------

Byte  = UBInt8
SChar = SLInt8
UChar = ULInt8
Char  = SChar

Int8  = SNInt8
Int16 = SNInt16
Int32 = SNInt32
Int64 = SNInt64

UInt8  = UNInt8
UInt16 = UNInt16
UInt32 = UNInt32
UInt64 = UNInt64

Float32  = NFloat32
Float64  = NFloat64

#------------------------------------------------------------------------
# Strings
#------------------------------------------------------------------------

class Sequence(Type):
    """ Fixed sequence of type ``ty`` with integral ``length``
    """

    def __init__(self, ty, length):
        if not isinstance(length, numbers.Integral):
            raise ValueError('Must be integral length')

        self.ty = ty
        self.length = length

    @property
    def name(self):
        return self.ty.name

    def to_dtype(self):
        return numpy.dtype((self.ty.to_dtype(), self.length))

    def to_llvm(self):
        return lc.Type.array(self.ty.to_llvm(), self.length)

    def to_ctypes(self):
        return self.ty.to_ctypes() * self.length

class VariableString(Type):

    def __init__(self, name):
        self.name = name

    def to_dtype(self):
        raise NoDtypeMapping(self)

    def to_llvm(self):
        return lc.Type.struct([
            lc.Type.int(8),
            lc.Type.int(8),
        ], name='vstring')

    def to_ctypes(self):
        class vstring(ctypes.Structure):
            _fields_ = [
                ('ptr', ctypes.c_void_p),
                ('offset', ctypes.c_int),
            ]
        return vstring

class TerminatedString(Type):

    def __init__(self, name, terminator):
        self.name = name
        self.terminator = terminator

    def to_ctypes(self):
        return ctypes.c_char_p

    def to_llvm(self):
        return lc.Type.pointer(lc.Type.int(8))

    def to_dtype(self):
        return numpy.str_

def FixedString(name, length):
    return Sequence(Char(name), length)

def CString(name):
    return TerminatedString(name, '0x00')

#------------------------------------------------------------------------
# LLArrays
#------------------------------------------------------------------------

def Array_C(name, ty, nd):
    return Struct('Array_C',
        Pointer(ty('data')),
        Sequence(UNInt8('shape'), nd),
    )

def Array_F(name, ty, nd):
    return Struct('Array_F',
        Pointer(ty('data')),
        Sequence(UNInt8('shape'), nd),
    )

def Array_S(name, ty, nd):
    return Struct('Array_S',
        Pointer(ty('data')),
        Sequence(UNInt8('shape'), nd),
        Sequence(UNInt8('stride'), nd),
    )

def Array_A(name, ty, nd):
    raise NotImplementedError
