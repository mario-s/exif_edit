from exif import ColorSpace

class Converter:

    @staticmethod
    def convert(key, value):
        if key == "color_space":
            return Converter.__convert_color_space(value)
        return value

    @staticmethod
    def __convert_color_space(value):
        if value == 1 or value == "1":
            return ColorSpace.SRGB
        return ColorSpace.UNCALIBRATED