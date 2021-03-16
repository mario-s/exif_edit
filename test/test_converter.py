import unittest
from exif import ColorSpace, ResolutionUnit, Orientation

from exif_edit.converter import Converter


class TestConverter(unittest.TestCase):

    def test_filter(self):
        keys = Converter.keys()
        self.assertTrue(len(keys) > 0)

    def test_convert_unknown(self):
        self.assertEqual(1, Converter.cast('foo', 1))

    def test_convert_color_space_srgb(self):
        self.assertEqual(ColorSpace.SRGB, Converter.cast("color_space", "SRGB"))

    def test_convert_color_space_uncalibrated(self):
        self.assertEqual(ColorSpace.UNCALIBRATED, Converter.cast("color_space", "UNCALIBRATED"))

    def test_convert_resolution_unit_centimeters(self):
        self.assertEqual(ResolutionUnit.CENTIMETERS, Converter.cast("resolution_unit", "CENTIMETERS"))

    def test_convert_resolution_unit_inches(self):
        self.assertEqual(ResolutionUnit.INCHES, Converter.cast("resolution_unit", "1"))
    
    def test_convert_orientations(self):
        self.assertEqual(Orientation.LEFT_BOTTOM, Converter.cast("orientation", "LEFT_BOTTOM"))

    def test_convert_orientations_numeric(self):
        self.assertEqual(Orientation.TOP_RIGHT, Converter.cast("orientation", "2"))

    def test_convert_orientations_default(self):
        self.assertEqual(Orientation.TOP_LEFT, Converter.cast("orientation", "9"))

    def test_convert_orientations_none(self):
        self.assertEqual(Orientation.TOP_LEFT, Converter.cast("orientation", None))

    def test_try_read(self):
        m = {'foo': 'bar'}
        self.assertIsNone(Converter.try_read(m, 'baz'))


if __name__ == '__main__':
    unittest.main()