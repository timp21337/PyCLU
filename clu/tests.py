import unittest
import os

from functools import wraps  # use this to preserve function signatures and docstrings
from collections import OrderedDict
from unittest.runner import TextTestRunner
from clu import *

requirements = {
    '01': 'Conversions must be reflexive',
    '02': 'Conversions must be symetric',
    '03': 'Conversions must be transitive',
    '04': 'Expressions may only be composed of differing units where subsequent units are smaller than preceding units.',
    '05': 'All length units must be convertible to each other',
    '06': 'Rounding errors must not fail comparisons',
    '07': 'There must be a mechanism to add new units',
    '08': 'An object must be creatable from a string representation',
    '09': 'Anticipated exceptions must be tested',
}




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
    """
    test_refs = {}

    def run(self, test):
        result = TextTestRunner.run(self, test)
        if isinstance(test, unittest.suite.TestSuite):
            self.print_matrix()
        return result

    def print_matrix(self):
        paraTests = OrderedDict()
        reqParaCount = {}
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
            out.write("<h2>%s - %s</h2>" % (p, requirements[p]))
            out.write("<ul>")
            for t in paraTests[p]:
                out.write("<li>%s</li>" % t)
            out.write("</ul>")
        out.write("")
        out.write("</body>")
        out.write("</html>")


class TestRequirements(unittest.TestCase):

    def setUp(self):
        pass

    @requirementRefs(['06'])
    def test_example(self):
        self.assertEqual(str(Length(6, 'm').to('yd')), '6.562 yd')
        self.assertEqual(str(Length(2.5, 'yd').to('in')), '90 in')

    @requirementRefs(['01'])
    def test_reflexive(self):
        self.assertEqual(Length(1.1, 'in'),Length(1.1, 'in'))

    @requirementRefs(['02'])
    def test_symetric(self):
        self.assertEqual(Length(1.1, 'yd').to('m'),
                         Length(1.00584 , 'm'))
        self.assertEqual(Length(1.00584 , 'm').to('yd'),
                         Length(1.1, 'yd'))

        self.assertEqual(Length(1.1, 'yd'),
                         Length(1.1, 'yd').to('m').to('yd'))


    @requirementRefs(['03'])
    def test_transitive(self):
        pass

    @requirementRefs(['04'])
    def test_concatenable(self):
        pass

    @requirementRefs(['05'])
    def test_convert_between_all_units(self):
        self.assertEquals(str(Length(1.1, 'yd').to('in')), "39.6 in")
        self.assertEquals(str(Length(1.1, 'yd').to('m')), "1.006 m")
        self.assertEquals(str(Length(1.1, 'm').to('yd')), "1.203 yd")
        self.assertEquals(str(Length(1.1, 'm').to('in')), "43.307 in")
        self.assertEquals(str(Length(110, 'in').to('yd')), "3.056 yd")
        self.assertEquals(str(Length(110, 'in').to('m')), "2.794 m")

    @requirementRefs(['06'])
    def test_rounding(self):
        self.assertEqual(Length(36, 'in'), Length(1, 'yd'))

    @requirementRefs(['07'])
    def test_add_feet(self):
        add_unit(LengthUnit('ft', 'feet', 0.3048))
        self.assertEqual(Length(12, 'in'), Length(1, 'ft'))

    @requirementRefs(['04','08'])
    def test_fromString(self):
        add_unit(LengthUnit('ft', 'feet', 0.3048))
        self.assertEqual(Length(12, 'in'), Length.fromString('1 ft'))
        self.assertEqual(Length(14, 'in'), Length.fromString('1 ft 2 in'))

if __name__ == '__main__':
    unittest.main(testRunner=RDDTestRunner)
