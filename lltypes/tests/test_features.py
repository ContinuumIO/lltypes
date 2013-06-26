import sys
import unittest
import numpy as np

is_py3k = bool(sys.version_info[0] == 3)

from lltypes import *

tests = []

#------------------------------------------------------------------------

class TestToplevel(unittest.TestCase):

    def test_struct_dtype(self):
        mystruct = Struct(
            'mystruct',
            Bool('a'),
            Int8('b'),
            Float32('c'),
        )
        self.assertEqual(
            mystruct.to_dtype(),
            np.dtype([('a', '?'), ('b', 'i1'), ('c', '<f4')])
        )

    def test_struct_llvm(self):
        mystruct = Struct(
            'mystruct',
            Bool('a'),
            Int8('b'),
            Float32('c'),
        )
        llstruct = mystruct.to_llvm()
        self.assertEqual(
            str(llstruct),
            """%mystruct = type { i1, i8, float }"""
        )

    def test_sequence(self):
        myarr = Sequence(Int8('a'), 128)

    def test_toplevle(self):
        c = Array_C('foo', UNInt8, 3)
        f = Array_F('foo', UNInt8, 3)
        s = Array_S('foo', UNInt8, 3)

        print(c.to_ctypes())
        print(f.to_ctypes())
        print(s.to_ctypes())

        print(c.to_dtype())
        print(f.to_dtype())
        print(s.to_dtype())

        print(c.to_llvm())
        print(f.to_llvm())
        print(s.to_llvm())

        print(Enum('bar',
            X = 1,
            Y = 2,
            Z = 3
        ).to_ctypes())

        print(Enum('bar',
            X = 1,
            Y = 2,
            Z = 3
        ).to_llvm())

        print(FixedString('foo', 35).to_llvm())
        print(FixedString('foo', 35).to_ctypes())
        print(FixedString('foo', 35).to_dtype())

        print(VariableString('foo').to_llvm())
        print(VariableString('foo').to_ctypes())


tests.append(TestToplevel)

#------------------------------------------------------------------------

def run(verbosity=1, repeat=1):
    suite = unittest.TestSuite()
    for cls in tests:
        for _ in range(repeat):
            suite.addTest(unittest.makeSuite(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

if __name__ == '__main__':
    run()
