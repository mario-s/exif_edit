"""
This module contains classes related to coordinates.
"""
import re
from typing import List, Tuple

class Format:
    def decimal_degrees(self):
        pass

    def dms_degrees(self):
        pass

class DmsFormat(Format):
    """
    Degree given in DMS format.
    """
    def __init__(self, degrees):
        if len(degrees) != 3:
            raise ValueError("expected (degree, minuntes, seconds)")
        self.degrees = (int(degrees[0]), int(degrees[1]), float(degrees[2]))

    def dms_degrees(self):
        return self.degrees

    def __dms2dec(self):
        deg = self.degrees[0]
        min = self.degrees[1]/60
        sec = self.degrees[2]/3600
        if deg >= 0:
            return deg + min + sec
        return deg - min - sec

    def decimal_degrees(self):
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

    def dms_degrees(self):
        """ 
        Converts decimal degrees to (degrees, minutes, and seconds).
        """
        deg = int(self.degrees)
        minutes = int((self.degrees - deg) * 60)
        sec = (self.degrees - deg - minutes/60) * 3600
        
        return deg, minutes, round(sec, 6)

    def decimal_degrees(self):
        return round(self.degrees, 6)
        
    def __repr__(self) -> str:
        return f"{self.decimal_degrees()}°"
    
class Factory:
    """
    Creates a new instance of a format
    """
    @staticmethod
    def create(degrees):
        if isinstance(degrees, Tuple) or isinstance(degrees, List):
            return DmsFormat(degrees)
        return DecimalFormat(degrees)

    @staticmethod
    def parse(arg):
        """
        Read a string and returns a matching format.
        """
        #DMS
        match = re.search('(\d+)°(\d+)\'(\d+.?\d*)\"', str(arg))
        if match:
            return DmsFormat((match.group(1), match.group(2), match.group(3)))
        
        #DEC
        match = re.search('(\d+.?\d*)°', str(arg))
        if match:
            return DecimalFormat(match.group(1))

        raise ValueError(f"unknown format for {arg}")

class Coordinate:
    """
    Represent a coordinate on the globe.
    """
    def __init__(self, latitude, longitude, lat_ref = 'N', lon_ref = 'E'):
        self.latitude = latitude
        self.lat_ref = lat_ref

        self.longitude = longitude
        self.lon_ref = lon_ref

    def decimal(self):
        lat_dec = abs(self.latitude.decimal_degrees())
        lon_dec = abs(self.longitude.decimal_degrees())
        lat = lat_dec if self.lat_ref == 'N' else -1 * lat_dec
        lon = lon_dec if self.lon_ref == 'E' else -1 * lon_dec
        return lat, lon