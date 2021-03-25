"""
This class holds the value of the latitude or longitude used in coordinates.
"""
class DmsFormat:
    def __init__(self, value):
        if len(value) != 3:
            raise ValueError("expected (degree, minuntes, seconds)")

        self.degrees = int(value[0])
        self.minutes = int(value[1])
        self.seconds = value[2]

    def __dms2dd(self):
        """ 
        Converts degrees, minutes, and seconds to decimal degrees.
        """
        min = self.minutes/60
        sec = self.seconds/3600
        if self.degrees >= 0:
            return self.degrees + min + sec
        return self.degrees - min - sec

    def decimalDegrees(self):
        return round(self.__dms2dd(), 6)

    def __repr__(self) -> str:
        return f"{self.degrees}°{self.minutes}\'{self.seconds}\""