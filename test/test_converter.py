import unittest
from exif import ColorSpace, ResolutionUnit

from exif_edit.converter import Converter


class TestConverter(unittest.TestCase):

    def setUp(self):
        self.converter = Converter()

    def test_converter_unknown(self):
        self.assertEqual(1, self.converter.convert('foo', 1))

    def test_converter_color_space_srgb(self):
        self.assertEqual(ColorSpace.SRGB, self.converter.convert("color_space", "1"))

    def test_converter_color_space_uncalibrated(self):
        self.assertEqual(ColorSpace.UNCALIBRATED, self.converter.convert("color_space", "0"))

    def test_converter_resolution_unit_centimeters(self):
        self.assertEqual(ResolutionUnit.CENTIMETERS, self.converter.convert("resolution_unit", "3"))

    def test_converter_resolution_unit_inches(self):
        self.assertEqual(ResolutionUnit.INCHES, self.converter.convert("resolution_unit", "1"))
    

if __name__ == '__main__':
    unittest.main()