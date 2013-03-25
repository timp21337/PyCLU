import unittest

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



testParas = {}

def requirementParas(paras):
    """See http://stackoverflow.com/questions/306130/python-decorator-makes-function-forget-that-it-belongs-to-a-class"""
    def logger(test):
        @wraps(test)
        def with_aggregation(*args, **kwargs):
            testParas[args[0].__class__.__name__ + "." + test.__name__] = paras
            return test(*args, **kwargs)
        return with_aggregation
    return logger


class RDDTestRunner(TextTestRunner):
    """
    A test runner to aggregate requirements paragraphs.
    """
    def run(self, test):
        result = TextTestRunner.run(self, test)
        if isinstance(test, unittest.suite.TestSuite):
            self.print_matrix()
        return result

    def print_matrix(self):
        paraTests = OrderedDict()
        reqParaCount = {}
        for test in testParas.keys():
            for para in testParas[test]:
                if para in paraTests:
                    paraTests[para].append(test)
                else:
                    paraTests[para] = [test]
        print("")
        print("<h1>Requirements Verification Matrix</h1>")
        for p in sorted(paraTests.keys()):
            print("<h2>%s - %s</h2>" % (p, requirements[p]))
            print "<ul>"
            for t in paraTests[p]:
                print("<li>%s</li>" % t)
            print "</ul>"
        print("")


class TestRequirements(unittest.TestCase):

    def setUp(self):
        pass

    @requirementParas(['06'])
    def test_example(self):
        self.assertEqual(str(Length(6, 'm').to('yd')), '6.562 yd')
        self.assertEqual(str(Length(2.5, 'yd').to('in')), '90 in')

    @requirementParas(['01'])
    def test_reflexive(self):
        self.assertEqual(Length(1.1, 'in'),Length(1.1, 'in'))

    @requirementParas(['02'])
    def test_symetric(self):
        self.assertEqual(Length(1.1, 'yd').to('m'),
                         Length(1.00584 , 'm'))
        self.assertEqual(Length(1.00584 , 'm').to('yd'),
                         Length(1.1, 'yd'))

        self.assertEqual(Length(1.1, 'yd'),
                         Length(1.1, 'yd').to('m').to('yd'))


    @requirementParas(['03'])
    def test_transitive(self):
        pass

    @requirementParas(['04'])
    def test_concatenable(self):
        pass

    @requirementParas(['05'])
    def test_convert_between_all_units(self):
        self.assertEquals(str(Length(1.1, 'yd').to('in')), "39.6 in")
        self.assertEquals(str(Length(1.1, 'yd').to('m')), "1.006 m")
        self.assertEquals(str(Length(1.1, 'm').to('yd')), "1.203 yd")
        self.assertEquals(str(Length(1.1, 'm').to('in')), "43.307 in")
        self.assertEquals(str(Length(110, 'in').to('yd')), "3.056 yd")
        self.assertEquals(str(Length(110, 'in').to('m')), "2.794 m")

    @requirementParas(['06'])
    def test_rounding(self):
        self.assertEqual(Length(36, 'in'), Length(1, 'yd'))

    @requirementParas(['07'])
    def test_add_feet(self):
        add_unit(LengthUnit('ft', 'feet', 0.3048))
        self.assertEqual(Length(12, 'in'), Length(1, 'ft'))

    @requirementParas(['04','08'])
    def test_fromString(self):
        add_unit(LengthUnit('ft', 'feet', 0.3048))
        self.assertEqual(Length(12, 'in'), Length.fromString('1 ft'))
        self.assertEqual(Length(14, 'in'), Length.fromString('1 ft 2 in'))

if __name__ == '__main__':
    unittest.main(testRunner=RDDTestRunner)
