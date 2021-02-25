import unittest
from exif import ColorSpace, ResolutionUnit

from exif_edit.converter import Converter


class TestConverter(unittest.TestCase):

    def test_converter_unknown(self):
        self.assertEqual(1, Converter.convert('foo', 1))

    def test_converter_color_space_srgb(self):
        self.assertEqual(ColorSpace.SRGB, Converter.convert("color_space", "1"))

    def test_converter_color_space_uncalibrated(self):
        self.assertEqual(ColorSpace.UNCALIBRATED, Converter.convert("color_space", "0"))

    def test_converter_resolution_unit_centimeters(self):
        self.assertEqual(ResolutionUnit.CENTIMETERS, Converter.convert("resolution_unit", "3"))

    def test_converter_resolution_unit_inches(self):
        self.assertEqual(ResolutionUnit.INCHES, Converter.convert("resolution_unit", "1"))
    
if __name__ == '__main__':
    unittest.main()