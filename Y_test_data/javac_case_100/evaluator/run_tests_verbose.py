from __future__ import print_function

import sys
import unittest


if __name__ == '__main__':
    suite = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stdout.flush()
    sys.stderr.flush()
    # JEP 3.2 treats any Python SystemExit as an embedding exception,
    # including SystemExit(0). Return naturally on success instead.
    if not result.wasSuccessful():
        raise AssertionError("test suite failed")
