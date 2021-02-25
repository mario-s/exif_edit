from exif import ColorSpace, ResolutionUnit, Orientation


class Converter:
    def __init__(self):
        #the first key, value pair is used as a fall back for an illegal input
        self.color_spaces = {"2": ColorSpace.UNCALIBRATED, "1": ColorSpace.SRGB}
        self.resolution_units = {"2": ResolutionUnit.INCHES, "3": ResolutionUnit.CENTIMETERS}
        self.orientations = {
            "1": Orientation.TOP_LEFT, "2": Orientation.TOP_RIGHT,
            "3": Orientation.BOTTOM_RIGHT, "4": Orientation.BOTTOM_LEFT,
            "5": Orientation.LEFT_TOP, "6": Orientation.RIGHT_TOP,
            "7": Orientation.RIGHT_BOTTOM, "8": Orientation.LEFT_BOTTOM}

    def convert(self, key, value):
        if key == "color_space":
            return self.__lookup(self.color_spaces, value)
        elif key == "resolution_unit":
            return self.__lookup(self.resolution_units, value)
        elif key == "orientation":
            return self.__lookup(self.orientations, value)
        return value

    def __lookup(self, dict, value):
        try:
            return dict[value]
        except:
            k = next(iter(dict))
            return dict[k]
