import unittest
from exif import ColorSpace, ResolutionUnit, Orientation

from exif_edit.converter import Converter
from exif_edit.geoloc import Factory


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

    def test_rows_to_dict(self):
        rows = [["model", "bar"]]
        d = Converter.rows_to_dict(rows)
        self.assertDictEqual({'model': 'bar'}, d)

    def test_grouped_dict(self):
        d = {"b": 1, "a": 2, "exif_version": 22}
        r = Converter.group_dict(d)
        self.assertEqual({"exif_version": 22, "a": 2, "b": 1}, r)

    def test_cast_dms(self):
        loc = Factory.create([78.0, 55.0, 44.33324])
        r = Converter.cast('', loc)
        self.assertIsInstance(r, tuple)

    def test_illegal_degree(self):
        dic = {'gps_latitude': 'a'}
        self.assertIsNone(Converter.try_read(dic, 'gps_latitude'))

if __name__ == '__main__':
    unittest.main()