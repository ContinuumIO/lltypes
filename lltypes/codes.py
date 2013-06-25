import ctypes
import struct
import llvm.core as lc

format_ctypes = {
    'c'	: ctypes.c_char,
    'b'	: ctypes.c_byte,
    'B'	: ctypes.c_ubyte,
    '?'	: ctypes.c_bool,
    'h'	: ctypes.c_short,
    'H'	: ctypes.c_ushort,
    'i'	: ctypes.c_int,
    'I'	: ctypes.c_uint,
    'l'	: ctypes.c_long,
    'L'	: ctypes.c_ulong,
    'Q'	: ctypes.c_longlong,
    'f'	: ctypes.c_float,
    'd'	: ctypes.c_double,
    's'	: ctypes.c_char_p,
    'p'	: ctypes.c_char_p,
    'P'	: ctypes.c_void_p,
}

format_llvm = {
    'c'	: lc.Type.int(8),
    'b'	: lc.Type.int(8),
    'B'	: lc.Type.int(8),
    '?'	: lc.Type.int(1),
    #'h'	: ctypes.c_short,
    #'H'	: ctypes.c_ushort,
    'i'	: lc.Type.int(8),
    'I'	: lc.Type.int(8),
    #'l'	: ctypes.c_long,
    #'L'	: ctypes.c_ulong,
    #'Q'	: ctypes.c_longlong,
    'f'	: lc.Type.float(),
    'd'	: lc.Type.double(),
    's'	: lc.Type.pointer(lc.Type.int(8)),
    'p'	: lc.Type.pointer(lc.Type.int(8)),
    #'P'	: ,
}
