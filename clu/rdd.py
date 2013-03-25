"""Requirements Driven Development"""
__author__ = 'timp21337'

import unittest
import os

from functools import wraps  # use this to preserve function signatures and docstrings
from collections import OrderedDict
from unittest.runner import TextTestRunner

_requirements = {}


def add_requirement(ref, desc):
    """Add a requirement"""
    _requirements[ref] = desc


def requirementRefs(refs):
    """See http://stackoverflow.com/questions/306130/python-decorator-makes-function-forget-that-it-belongs-to-a-class"""
    def logger(test):
        @wraps(test)
        def with_aggregation(*args, **kwargs):
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
        paraTests = OrderedDict()
        for test in self.test_refs.keys():
            for para in self.test_refs[test]:
                if para in paraTests:
                    paraTests[para].append(test)
                else:
                    paraTests[para] = [test]
        directory = 'Requirements_Verification_Matrix'
        if not os.path.exists(directory):
            os.makedirs(directory)

        out = open('%s/index.html' % directory, 'w')
        out.write("<html>")
        out.write("<body>")
        out.write("<h1>Requirements Verification Matrix</h1>")
        for p in sorted(paraTests.keys()):
            out.write("<h2>%s - %s</h2>" % (p, _requirements[p]))
            out.write("<ul>")
            for t in paraTests[p]:
                out.write("<li>%s</li>" % t)
            out.write("</ul>")
        out.write("")
        out.write("</body>")
        out.write("</html>")

