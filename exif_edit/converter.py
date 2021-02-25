from exif import ColorSpace, ResolutionUnit

class Converter:

    @staticmethod
    def convert(key, value):
        if key == "color_space":
            return Converter.__to_color_space(value)
        elif key == "resolution_unit":
            return Converter.__to_resolution_unit(value)
        return value

    @staticmethod
    def __to_color_space(value):
        if value == "1":
            return ColorSpace.SRGB
        return ColorSpace.UNCALIBRATED

    @staticmethod
    def __to_resolution_unit(value):
        if value == "3":
            return ResolutionUnit.CENTIMETERS
        return ResolutionUnit.INCHES