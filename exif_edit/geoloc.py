class LocationFormat:
    def __init__(self, value):
        if isinstance(value, tuple):
            #degrees, minutes, seconds
            if len(value) == 3:
                self.format = self.__dms2decimal(value[0], value[1], value[2])
            #degrees and decimal minutes
            else:
                pass
        #decimal degrees
        else:
            self.format = value

    @classmethod
    def __dms2decimal(cls, degrees, minutes, seconds):
        """ 
        Converts degrees, minutes, and seconds to decimal degrees.
        """

        dec = degrees
        min = minutes/60
        sec = seconds/3600
        if degrees >= 0:
            dec = dec + min + sec
        else:
            dec = dec - min - sec
        
        return round(dec, 6)
            

    def decimalDegrees(self):
        return self.format