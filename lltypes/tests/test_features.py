import sys
import unittest

is_py3k = bool(sys.version_info[0] == 3)

import lltypes

tests = []

#------------------------------------------------------------------------

class TestToplevel(unittest.TestCase):
    pass


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
