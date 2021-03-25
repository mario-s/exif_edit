"""
This module contains classes related to coordinates.
"""
class DmsFormat:
    """
    Degree given in DMS format.
    """
    def __init__(self, value):
        if len(value) != 3:
            raise ValueError("expected (degree, minuntes, seconds)")

        self.degrees = int(value[0])
        self.minutes = int(value[1])
        self.seconds = value[2]

    def __dms2dec(self):
        min = self.minutes/60
        sec = self.seconds/3600
        if self.degrees >= 0:
            return self.degrees + min + sec
        return self.degrees - min - sec

    def decimalDegrees(self):
        """ 
        Converts degrees, minutes, and seconds to decimal degrees.
        """
        return round(self.__dms2dec(), 6)

    def __repr__(self) -> str:
        return f"{self.degrees}°{self.minutes}\'{self.seconds}\""

class DecimalFormat:
    """
    Degree given in Decimal format.
    """
    def __init__(self, value):
        if value is None:
            raise ValueError("expected degree in decimal")

        self.degrees = value

    def dmsDegrees(self):
        """ 
        Converts decimal degrees to (degrees, minutes, and seconds).
        """
        deg = int(self.degrees)
        min = int((self.degrees - deg) * 60)
        sec = (self.degrees - deg - min/60) * 3600
        
        return deg, min, round(sec, 6)
        
    def __repr__(self) -> str:
        return f"{round(self.degrees, 6)}°"