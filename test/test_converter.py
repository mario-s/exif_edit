import unittest
from exif import ColorSpace, ResolutionUnit, Orientation

from exif_edit.converter import Converter


class TestConverter(unittest.TestCase):

    def setUp(self):
        self.converter = Converter()

    def test_convert_unknown(self):
        self.assertEqual(1, self.converter.to_enumeration('foo', 1))

    def test_convert_color_space_srgb(self):
        self.assertEqual(ColorSpace.SRGB, self.converter.to_enumeration("color_space", "1"))

    def test_convert_color_space_uncalibrated(self):
        self.assertEqual(ColorSpace.UNCALIBRATED, self.converter.to_enumeration("color_space", "0"))

    def test_convert_resolution_unit_centimeters(self):
        self.assertEqual(ResolutionUnit.CENTIMETERS, self.converter.to_enumeration("resolution_unit", "3"))

    def test_convert_resolution_unit_inches(self):
        self.assertEqual(ResolutionUnit.INCHES, self.converter.to_enumeration("resolution_unit", "1"))
    
    def test_convert_orientations(self):
        self.assertEqual(Orientation.LEFT_BOTTOM, self.converter.to_enumeration("orientation", "8"))

    def test_convert_orientations_default(self):
        self.assertEqual(Orientation.TOP_LEFT, self.converter.to_enumeration("orientation", "9"))


if __name__ == '__main__':
    unittest.main()