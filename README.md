lltypes
=======

A type system for Python backed by llvm and ctypes

This project is a wrapping for spelling and translating between
ctypes, LLVM types and Numpy dtype.

Example: Structs
----------------

In C99 we might define the following structure:

```c
struct {
   bool a;
   int b;
   float c;
} mystruct;
```

We can map this structure in Python:

```python
from lltypes import *
mystruct = Struct(
    'mystruct',
    Bool('a'),
    Int32('b'),
    Float32('c'),
)
```

Which can be converted to ctypes using ``to_ctypes``:

```python
mycstruct = mystruct.to_ctypes()

inst = mycstruct(
    True,
    3,
    3.14
)

>>> inst.a
True
>>> inst.b
3
>>> inst.c
3.140000104904175
```

And to LLVM using ``to_llvm``:

```python
llstruct = mystruct.to_llvm()

>>> print llstruct
%mystruct = type { i1, i32, float }
```

And to dtype using ``to_dtype``:

```python
dtstruct = mystruct.to_dtype()

>>> print dtstruct
dtype([('a', '?'), ('b', 'i32'), ('c', '<f4')])
```

Example: Arrays
----------------

Blaze defines a family of parameterized types for its array
objects. These are first class polytypes in lltypes with the
following schema:

```ocaml
nd := 1 | 2 | 3 | 4 | 5

mono := Byte | Int8 | Int32 | ...

poly := Array_C <mono> <nd>
      | Array_F <mono> <nd>
      | Array_S <mono> <nd>
```

In C these are structures of array kinds parameterized by ``eltype``
and ``nd``.


```c
// Contiguous or Fortran
struct {
   eltype *data;
   intp shape[nd];
} Array_C;

struct {
   eltype *data;
   diminfo shape[nd];
} Array_F;

struct {
   eltype *data;
   intp shape[nd];
   intp stride[nd];
} Array_S;
```

In lltypes these are expanded out into lower types by a simple
function.

```python
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
```

```python
>>> c = Array_C('foo', UNInt8, 3)
>>> f = Array_F('foo', UNInt8, 3)
>>> s = Array_S('foo', UNInt8, 3)

>>> print c.to_llvm()
%Array_C = type { i8*, [3 x i8] }
>>> print f.to_llvm()
%Array_F = type { i8*, [3 x i8] }
>>> print s.to_llvm()
%Array_S = type { i8*, [3 x i8], [3 x i8] }
```

Tests
-----

Test suite can be run with either of the following:

```bash
python -m unittest discover
```

or:

```python
from lltypes import test
test()
```

