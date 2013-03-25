"""Tests for clu"""

import unittest

from .rdd import RDDTestRunner
from .rdd import requirement_refs
from .rdd import add_requirement

from .clu import Length
from .clu import LengthUnit
from .clu import get_unit
from .clu import add_unit

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
    """All tests - annotated with requirement id."""

    @requirement_refs(['06'])
    def test_example(self):
        self.assertEqual(str(Length(6, 'm').to('yd')), '6.562 yd')
        self.assertEqual(str(Length(2.5, 'yd').to('in')), '90 in')

    @requirement_refs(['01'])
    def test_reflexive(self):
        self.assertEqual(Length(1.1, 'in'), Length(1.1, 'in'))

    @requirement_refs(['02'])
    def test_symetric(self):
        self.assertEqual(Length(1.1, 'yd').to('m'),
                         Length(1.00584, 'm'))
        self.assertEqual(Length(1.00584, 'm').to('yd'),
                         Length(1.1, 'yd'))

        self.assertEqual(Length(1.1, 'yd'),
                         Length(1.1, 'yd').to('m').to('yd'))


    @requirement_refs(['03'])
    def test_transitive(self):
        """If x = y and y = z then x = z"""
        self.assertEqual(Length(1.1, 'yd').to('m').to('in'),
                         Length(39.6, 'in'))
        self.assertEqual(Length(39.6, 'in').to('m').to('yd'),
                         Length(1.1, 'yd'))

    @requirement_refs(['04'])
    def test_concatenable(self):
        add_unit(LengthUnit('ft', 'feet', 0.3048))
        self.assertEqual(Length(170, 'in'), Length.from_string('4 yd 2 ft 2 in'), Length.from_string('4 yd 2 ft 2 in'))
        self.assertRaises(StandardError, Length.from_string, '2 in 4 ft')

    @requirement_refs(['05'])
    def test_convert_between_all_units(self):
        self.assertEquals(str(Length(1.1, 'yd').to('in')), "39.6 in")
        self.assertEquals(str(Length(1.1, 'yd').to('m')), "1.006 m")
        self.assertEquals(str(Length(1.1, 'm').to('yd')), "1.203 yd")
        self.assertEquals(str(Length(1.1, 'm').to('in')), "43.307 in")
        self.assertEquals(str(Length(110, 'in').to('yd')), "3.056 yd")
        self.assertEquals(str(Length(110, 'in').to('m')), "2.794 m")

    @requirement_refs(['06'])
    def test_rounding(self):
        self.assertEqual(Length(36, 'in'), Length(1, 'yd'))

    @requirement_refs(['07'])
    def test_add_feet(self):
        add_unit(LengthUnit('ft', 'feet', 0.3048))
        self.assertEqual(Length(12, 'in'), Length(1, 'ft'))

    @requirement_refs(['04', '08'])
    def test_from_string(self):
        add_unit(LengthUnit('ft', 'feet', 0.3048))
        self.assertEqual(Length(12, 'in'), Length.from_string('1 ft'))
        self.assertEqual(Length(14, 'in'), Length.from_string('1 ft 2 in'))

    def test_compare_with_differing_type(self):
        try:
            Length('1 in') == get_unit('in')
            self.fail("Should have bombed")
        except TypeError:
            pass


if __name__ == '__main__':
    unittest.main(testRunner=RDDTestRunner)
