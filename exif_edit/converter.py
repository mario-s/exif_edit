from exif import ColorSpace, ResolutionUnit, Orientation


class Converter:
    def __init__(self):
        #the first key, value pair is used as a fall back for an illegal input
        color_spaces = {"2": ColorSpace.UNCALIBRATED, "1": ColorSpace.SRGB}
        resolution_units = {"2": ResolutionUnit.INCHES, "3": ResolutionUnit.CENTIMETERS}
        orientations = {
            "1": Orientation.TOP_LEFT, "2": Orientation.TOP_RIGHT,
            "3": Orientation.BOTTOM_RIGHT, "4": Orientation.BOTTOM_LEFT,
            "5": Orientation.LEFT_TOP, "6": Orientation.RIGHT_TOP,
            "7": Orientation.RIGHT_BOTTOM, "8": Orientation.LEFT_BOTTOM}

        self.dictionary = {"color_space": color_spaces, 
            "resolution_unit": resolution_units,
            "orientation": orientations}

    def to_enumeration(self, key, value):
        if key in self.dictionary:
            dict = self.dictionary[key]
            return self.__lookup(dict, value)
        return value

    def __lookup(self, dict, value):
        if value in dict:
            return dict[value]
        #return first
        k = next(iter(dict))
        return dict[k]
