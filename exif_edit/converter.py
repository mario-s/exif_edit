import exif as ex

class Converter:

    """This class converts between the human readable values and the Enum values."""

    def __init__(self):
        self.dict = {"color_space": ex.ColorSpace, 
            "exposure_mode": ex.ExposureMode,
            "resolution_unit": ex.ResolutionUnit,
            "orientation": ex.Orientation}

    def to_enumeration(self, key, value):
        #do we have a matching enum in our dictionary?
        if key in self.dict:
            en = self.dict[key]
            #is the value a valid enum name?
            if value in en.__members__:
                return en[value]
            #fallback to first enum value
            return list(en)[0]

        return value
