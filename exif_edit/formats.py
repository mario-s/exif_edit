"""
This module contains custom formats used in the GUI.
"""
import re
from typing import List, Tuple

class Format:
    """
    Parent class for every format.
    """
    def __init__(self, source):
        self.source = source

    def get_source(self):
        """
        This will return the underlying source value."
        """
        return self.source

class TimeStamp(Format):
    """
    A time stamp made from a tupel.
    """
    def __init__(self, val, separator = ':'):
        if len(val) != 3:
            raise ValueError("expected (hour, minuntes, seconds)")
        super().__init__((int(val[0]), int(val[1]), int(val[2])))
        self.sepr = separator

    def __repr__(self) -> str:
        return f"{self.source[0]:02d}{self.sepr}{self.source[1]:02d}{self.sepr}{self.source[2]:02d}"

    @staticmethod
    def parse(value):
        if isinstance(value, (List, Tuple)):
            return TimeStamp(value)

        match = re.search(r"(\d+):(\d+):(\d+)", str(value))
        if match:
            return TimeStamp((match.group(1), match.group(2), match.group(3)))

        raise ValueError(f"can't parse given value: {value}")


class DegreeFormat(Format):
    """
    Format for a degree.
    """
    def as_float(self) -> float:
        """
        This will return the value as a single float number.
        """

    def as_tupel(self) -> Tuple:
        """
        Returns the format as a tuple of degree, minute, seconds.
        """

class DmsFormat(DegreeFormat):
    """
    Degree given in DMS format.
    """
    def __init__(self, degrees):
        if len(degrees) != 3:
            raise ValueError("expected (degree, minuntes, seconds)")
        super().__init__(tuple(degrees))

    def as_float(self) -> float:
        """
        Converts degrees, minutes, and seconds to decimal degrees.
        """
        return round(self.__dms2dec(), 6)

    def as_tupel(self) -> tuple:
        return super().get_source()

    def __dms2dec(self):
        deg = int(self.source[0])
        mnt = int(self.source[1])/60
        sec = float(self.source[2])/3600
        if deg >= 0:
            return deg + mnt + sec
        return deg - mnt - sec

    def __repr__(self) -> str:
        return f"{int(self.source[0])}°{int(self.source[1])}\'{float(self.source[2])}\""

class DecimalFormat(DegreeFormat):
    """
    Degree given in Decimal format.
    """
    def __init__(self, degree):
        if degree is None:
            raise ValueError("expected degree in decimal")

        super().__init__(float(degree))

    def as_tuple(self) -> Tuple:
        """
        Converts decimal degrees to (degrees, minutes, and seconds).
        """
        deg = int(self.source)
        mnt = int((self.source - deg) * 60)
        sec = (self.source - deg - mnt/60) * 3600

        return deg, mnt, round(sec, 6)

    def as_float(self):
        return round(super().get_source(), 6)

    def __repr__(self) -> str:
        return f"{self.as_float()}°"

class DegreeFormatFactory:
    """
    Creates a new instance of a format
    """
    @staticmethod
    def create(degrees):
        """
        This method create a new Format by matching against the type.
        """
        #already in the right format
        if isinstance(degrees, DegreeFormat):
            return degrees

        if isinstance(degrees, (List, Tuple)):
            return DmsFormat(degrees)
        if isinstance(degrees, (float, int)):
            return DecimalFormat(degrees)
        if isinstance(degrees, str):
            return DegreeFormatFactory.parse(degrees)

        raise ValueError("can't handle given type")

    @staticmethod
    def parse(arg):
        """
        Read a string and returns a matching format.
        """
        #DMS
        match = re.search(r"(\d+)°(\d+)\'(\d+.?\d*)\"", str(arg))
        if match:
            return DmsFormat((match.group(1), match.group(2), match.group(3)))

        #DEC
        match = re.search(r"(\d+.?\d*)°?", str(arg))
        if match:
            return DecimalFormat(match.group(1))

        raise ValueError(f"unknown format to parse degree: {arg}")
