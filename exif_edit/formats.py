"""
This module contains classes related to GPS data.
"""
import re
from typing import List, Tuple

class Format:
    """
    Parent class for degree format.
    """
    def as_float(self) -> float:
        """
        This will return the value as a single float number.
        """
        pass

    def as_tuple(self) -> tuple:
        """
        This will return the format as a tuple in terms of DMS it means °\'\""
        """
        pass

class TimeStamp(Format):
    """
    A time stamp made from a tupel.
    """
    def __init__(self, tpl, separator = ':'):
        if len(tpl) != 3:
            raise ValueError("expected (hour, minuntes, seconds)")
        self.val = (int(tpl[0]), int(tpl[1]), int(tpl[2]))
        self.separ = separator

    def as_tuple(self):
        return self.val

    def __repr__(self) -> str:
        return f"{self.val[0]:02d}{self.separ}{self.val[1]:02d}{self.separ}{self.val[2]:02d}"

    @staticmethod
    def parse(value):
        if isinstance(value, (List, Tuple)):
            return TimeStamp(value)

        match = re.search(r"(\d+):(\d+):(\d+)", str(value))
        if match:
            return TimeStamp((match.group(1), match.group(2), match.group(3)))


class DmsFormat(Format):
    """
    Degree given in DMS format.
    """
    def __init__(self, degrees):
        if len(degrees) != 3:
            raise ValueError("expected (degree, minuntes, seconds)")
        self.degrees = (int(degrees[0]), int(degrees[1]), float(degrees[2]))

    def as_tuple(self) -> tuple:
        return self.degrees

    def __dms2dec(self):
        deg = self.degrees[0]
        mnt = self.degrees[1]/60
        sec = self.degrees[2]/3600
        if deg >= 0:
            return deg + mnt + sec
        return deg - mnt - sec

    def as_float(self) -> float:
        """
        Converts degrees, minutes, and seconds to decimal degrees.
        """
        return round(self.__dms2dec(), 6)

    def __repr__(self) -> str:
        return f"{self.degrees[0]}°{self.degrees[1]}\'{self.degrees[2]}\""

class DecimalFormat(Format):
    """
    Degree given in Decimal format.
    """
    def __init__(self, degree):
        if degree is None:
            raise ValueError("expected degree in decimal")

        self.degrees = float(degree)

    def as_tuple(self) -> tuple:
        """
        Converts decimal degrees to (degrees, minutes, and seconds).
        """
        deg = int(self.degrees)
        mnt = int((self.degrees - deg) * 60)
        sec = (self.degrees - deg - mnt/60) * 3600

        return deg, mnt, round(sec, 6)

    def as_float(self) -> float:
        return round(self.degrees, 6)

    def __repr__(self) -> str:
        return f"{self.as_float()}°"

class DegreeFormatFactory:
    """
    Creates a new instance of a format
    """
    @staticmethod
    def create(degrees):
        #already in the right format
        if isinstance(degrees, Format):
            return degrees

        if isinstance(degrees, (List, Tuple)):
            return DmsFormat(degrees)
        if isinstance(degrees, (float, int)):
            return DecimalFormat(degrees)
        if isinstance(degrees, str):
            return DegreeFormatFactory.parse(degrees)

        raise ValueError("cant not handle given type")

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

        raise ValueError("unknown format to parse degree")
