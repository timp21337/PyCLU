__author__ = "timp"
__doc__ = """Length conversion utility"""


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

lengthUnits = {
    'in': LengthUnit('in', 'inches', 0.0254),
    'm': LengthUnit('m', 'metres', 1.0),
    'yd': LengthUnit('yd', 'yards', 0.9144)
}


def add_unit(unit):
    """Add a unit to the known units"""
    lengthUnits[unit.symbol] = unit


class Length(object):
    """A tuple of a real and a unit to represent a length."""

    def __init__(self, real, unitSymbol):
        self.real = real
        self.unit = lengthUnits[unitSymbol]

    @classmethod
    def fromString(cls, string):
        string = string.strip()
        (real_s, _, tail) = string.partition(' ')
        (unitSymbol, _, tail) = tail.partition(' ')
        real = float(real_s)
        unit = lengthUnits[unitSymbol]
        while tail != '':
            soFar = Length(real, unit.symbol)
            (real_s, _, tail) = tail.partition(' ')
            (unitSymbol, _, tail) = tail.partition(' ')
            nextLength = Length(float(real_s), unitSymbol)
            added = soFar + nextLength
            real = added.real
            unit = added.unit
        return Length(real, unit.symbol)

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

    def to(self, unitSymbol):
        return Length(((self.real * self.unit.metres)
                       / lengthUnits[unitSymbol].metres), unitSymbol)
