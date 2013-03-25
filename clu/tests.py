import unittest

import rdd
from rdd import requirementRefs
from rdd import add_requirement

from clu import *

add_requirement('01', 'Conversions must be reflexive.')
add_requirement('02', 'Conversions must be symetric.')
add_requirement('03', 'Conversions must be transitive.')
add_requirement('04', 'Expressions may only be composed of units where subsequent units are smaller than preceding.')
add_requirement('05', 'All length units must be convertible to each other.')
add_requirement('06', 'Rounding errors must not fail comparisons.')
add_requirement('07', 'There must be a mechanism to add new units.')
add_requirement('08', 'An object must be creatable from a string representation.')
add_requirement('09', 'Anticipated exceptions must be tested.')




class TestRequirements(unittest.TestCase):

    def setUp(self):
        pass

    @requirementRefs(['06'])
    def test_example(self):
        self.assertEqual(str(Length(6, 'm').to('yd')), '6.562 yd')
        self.assertEqual(str(Length(2.5, 'yd').to('in')), '90 in')

    @requirementRefs(['01'])
    def test_reflexive(self):
        self.assertEqual(Length(1.1, 'in'), Length(1.1, 'in'))

    @requirementRefs(['02'])
    def test_symetric(self):
        self.assertEqual(Length(1.1, 'yd').to('m'),
                         Length(1.00584, 'm'))
        self.assertEqual(Length(1.00584, 'm').to('yd'),
                         Length(1.1, 'yd'))

        self.assertEqual(Length(1.1, 'yd'),
                         Length(1.1, 'yd').to('m').to('yd'))


    @requirementRefs(['03'])
    def test_transitive(self):
        """If x = y and y = z then x = z"""
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

    @requirementRefs(['04', '08'])
    def test_fromString(self):
        add_unit(LengthUnit('ft', 'feet', 0.3048))
        self.assertEqual(Length(12, 'in'), Length.from_string('1 ft'))
        self.assertEqual(Length(14, 'in'), Length.from_string('1 ft 2 in'))

if __name__ == '__main__':
    unittest.main(testRunner=rdd.RDDTestRunner)
