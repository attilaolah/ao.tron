import doctest
import unittest


docfiles = [
    'input.txt',
    'board.txt',
]

def test_suite():
    """This is the test siute we use to run tests."""
    tests = [doctest.DocFileSuite(file,
        optionflags=doctest.ELLIPSIS) for file in docfiles]
    return unittest.TestSuite(tests)
