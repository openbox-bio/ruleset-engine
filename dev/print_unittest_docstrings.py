import unittest
import inspect
from pathlib import Path

'''
A script to list all the unit tests and associated docstrings in the tests folder.
'''

OUTPUT_FILE = "unit_test_descriptions.txt"

def extract_unittest_docstrings(test_dir: str):
    """
    Discover all unittest.TestCase tests under test_dir
    and write their names and docstrings to a single file.
    """
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for test in iter_tests(suite):
            test_method = getattr(test, test._testMethodName)
            doc = inspect.getdoc(test_method) or "(No docstring)"

            f.write(f"{test.__class__.__name__}.{test._testMethodName}\n")
            f.write(doc + "\n")
            f.write("-" * 80 + "\n")


def iter_tests(suite):
    """Recursively iterate through a unittest TestSuite."""
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_tests(item)
        else:
            yield item


if __name__ == "__main__":
    extract_unittest_docstrings("tests")  # path to your test folder
