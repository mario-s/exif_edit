"""
This class holds the value of the latitude or longitude used in coordinates.
"""
class Degree:
    def __init__(self, value):
        if value is None:
            raise ValueError("expected at value")

        if self.__is_collection(value):
            #degrees, minutes, seconds
            if len(value) == 3:
                self.format = self.__dms2dd(value[0], value[1], value[2])
        else:
            #decimal degrees
            self.format = value

    @classmethod
    def __is_collection(cls, value):
        return isinstance(value, tuple) or isinstance(value, list)

    @classmethod
    def __dms2dd(cls, degrees, minutes, seconds):
        """ 
        Converts degrees, minutes, and seconds to decimal degrees.
        """
        min = minutes/60
        sec = seconds/3600
        if degrees >= 0:
            return degrees + min + sec
        return degrees - min - sec

    def decimalDegrees(self):
        return round(self.format, 6)