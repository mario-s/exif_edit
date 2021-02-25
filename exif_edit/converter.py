from exif import ColorSpace, ResolutionUnit, Orientation


class Converter:
    def __init__(self):
        self.orientations = {"8": Orientation.LEFT_BOTTOM, "7": Orientation.RIGHT_BOTTOM, 
            "6": Orientation.RIGHT_TOP, "5": Orientation.LEFT_TOP, "4": Orientation.BOTTOM_LEFT,
            "3": Orientation.BOTTOM_RIGHT, "2": Orientation.TOP_RIGHT, "1": Orientation.TOP_LEFT}

    def convert(self, key, value):
        if key == "color_space":
            return self.__to_color_space(value)
        elif key == "resolution_unit":
            return self.__to_resolution_unit(value)
        elif key == "orientation":
            return self.__to_orientation(value)
        return value

    def __to_color_space(self, value):
        if value == "1":
            return ColorSpace.SRGB
        return ColorSpace.UNCALIBRATED

    def __to_resolution_unit(self, value):
        if value == "3":
            return ResolutionUnit.CENTIMETERS
        return ResolutionUnit.INCHES

    def __to_orientation(self, value):
        v = self.orientations[value]
        if v is None:
            return Orientation.LEFT_TOP
        return v