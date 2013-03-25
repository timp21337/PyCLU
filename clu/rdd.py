"""Requirements Driven Development"""
__author__ = 'timp21337'

import unittest
import os
from time import gmtime, strftime

from functools import wraps  # preserve function signatures and docstrings
from collections import OrderedDict
from unittest.runner import TextTestRunner

_REQUIREMENTS = {}


def add_requirement(ref, desc):
    """Add a requirement"""
    _REQUIREMENTS[ref] = desc


def requirement_refs(refs):
    """
    See
    http://stackoverflow.com/questions/306130/python-decorator-makes-function-forget-that-it-belongs-to-a-class
    """
    def logger(test):
        """Log each test."""
        @wraps(test)
        def with_aggregation(*args, **kwargs):
            """Aggregate its requirements."""
            RDDTestRunner.test_refs[args[0].__class__.__name__ + "." + test.__name__] = refs
            return test(*args, **kwargs)
        return with_aggregation
    return logger


class RDDTestRunner(TextTestRunner):
    """
    A test runner to aggregate requirements paragraphs.
    Requires a global dictionary called requirements.
    """
    test_refs = {}

    def run(self, test):
        result = TextTestRunner.run(self, test)
        if isinstance(test, unittest.suite.TestSuite):
            self.print_matrix()
        return result

    def print_matrix(self):
        """Print to an html output"""
        para_tests = OrderedDict()
        for test in self.test_refs.keys():
            for para in self.test_refs[test]:
                if para in para_tests:
                    para_tests[para].append(test)
                else:
                    para_tests[para] = [test]
        directory = 'Requirements_Verification_Matrix'
        if not os.path.exists(directory):
            os.makedirs(directory)

        out = open('%s/index.html' % directory, 'w')
        out.write("<html>\n")
        out.write("<body>\n")
        out.write("<h1>Requirements Verification Matrix</h1>\n")
        out.write("<h2>%s</h2>\n" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        for para in sorted(para_tests.keys()):
            out.write("<h3>%s - %s</h3>\n" % (para, _REQUIREMENTS[para]))
            out.write("<ul>\n")
            for test in para_tests[para]:
                out.write("<li>%s</li>\n" % test)
            out.write("</ul>\n")
        out.write("")
        out.write("</body>\n")
        out.write("</html>\n")

