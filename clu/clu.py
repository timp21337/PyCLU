"""Length conversion utility"""
__author__ = "timp21337"


class LengthUnit(object):
    """
    A definite magnitude of a physical quantity: length.
    """

    def __init__(self, symbol, name, metres):
        self.symbol = symbol
        self.name = name
        self.metres = metres

    def __lt__(self, other):
        return self.metres < other.metres

_LENGTH_UNITS = {
    'in': LengthUnit('in', 'inches', 0.0254),
    'm': LengthUnit('m', 'metres', 1.0),
    'yd': LengthUnit('yd', 'yards', 0.9144)
}


def add_unit(unit):
    """Add a unit to the known units"""
    _LENGTH_UNITS[unit.symbol] = unit


def get_unit(unit_symbol):
    return _LENGTH_UNITS[unit_symbol]


class Length(object):
    """A tuple of a real and a unit to represent a length."""

    def __init__(self, real, unit_symbol):
        self.real = real
        self.unit = _LENGTH_UNITS[unit_symbol]

    def __add__(self, other):
        if  other.unit < self.unit:
            return Length((self.to(other.unit.symbol).real + other.real), other.unit.symbol)
        else:
            raise StandardError("Subsequent units must be smaller")

    def __str__(self):
        string = "{:.3F}".format(self.real)
        string = string.strip('0')
        if string.startswith('.'):
            string = '0' + string
        if string.endswith('.'):
            string = string.strip('.')
        return "%s %s" % (string, self.unit.symbol)

    def __eq__(self, other):
        if isinstance(other, Length):
            return str(self.real * self.unit.metres) == str(other.real * other.unit.metres)
        else:
            raise TypeError(
                "Only objects of the same type can be compared for equality %s : %s" % (self, other))

    @classmethod
    def from_string(cls, string):
        """mint a Length usig for example '9 in'."""
        string = string.strip()
        (real_s, _, tail) = string.partition(' ')
        (unit_symbol, _, tail) = tail.partition(' ')
        real = float(real_s)
        unit = _LENGTH_UNITS[unit_symbol]
        while tail != '':
            so_far = Length(real, unit.symbol)
            (real_s, _, tail) = tail.partition(' ')
            (unit_symbol, _, tail) = tail.partition(' ')
            next_length = Length(float(real_s), unit_symbol)
            added = so_far + next_length
            real = added.real
            unit = added.unit
        return Length(real, unit.symbol)

    def to(self, unit_symbol):
        """Convert to given unit."""
        return Length(((self.real * self.unit.metres)
                       / _LENGTH_UNITS[unit_symbol].metres), unit_symbol)
