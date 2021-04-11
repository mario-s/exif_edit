import unittest
from exif import ColorSpace, ResolutionUnit, Orientation

from exif_edit.converter import Converter
from exif_edit.formats import DegreeFormatFactory


class TestConverter(unittest.TestCase):

    def test_filter(self):
        keys = Converter.keys()
        self.assertTrue(len(keys) > 0)

    def test_convert_unknown(self):
        self.assertEqual(1, Converter.to_exif('foo', 1))

    def test_convert_color_space_srgb(self):
        self.assertEqual(ColorSpace.SRGB, Converter.to_exif("color_space", "SRGB"))

    def test_convert_color_space_uncalibrated(self):
        self.assertEqual(ColorSpace.UNCALIBRATED, Converter.to_exif("color_space", "UNCALIBRATED"))

    def test_convert_resolution_unit_centimeters(self):
        self.assertEqual(ResolutionUnit.CENTIMETERS, Converter.to_exif("resolution_unit", "CENTIMETERS"))

    def test_convert_resolution_unit_inches(self):
        self.assertEqual(ResolutionUnit.INCHES, Converter.to_exif("resolution_unit", "1"))

    def test_convert_orientations(self):
        self.assertEqual(Orientation.LEFT_BOTTOM, Converter.to_exif("orientation", "LEFT_BOTTOM"))

    def test_convert_orientations_numeric(self):
        self.assertEqual(Orientation.TOP_RIGHT, Converter.to_exif("orientation", "2"))

    def test_convert_orientations_default(self):
        self.assertEqual(Orientation.TOP_LEFT, Converter.to_exif("orientation", "9"))

    def test_convert_orientations_none(self):
        self.assertEqual(Orientation.TOP_LEFT, Converter.to_exif("orientation", None))

    def test_try_read(self):
        m = {'foo': 'bar'}
        self.assertIsNone(Converter.read_from_dict(m, 'baz'))

    def test_rows_to_dict(self):
        rows = [["model", "bar"]]
        d = Converter.rows_to_dict(rows)
        self.assertDictEqual({'model': 'bar'}, d)

    def test_rows_to_dict_raise_error(self):
        rows = [["model"]]
        self.assertRaises(ValueError, lambda: Converter.rows_to_dict(rows))

    def test_grouped_dict(self):
        d = {"b": 1, "a": 2, "exif_version": 22}
        r = Converter.group_dict(d)
        self.assertEqual({"exif_version": 22, "a": 2, "b": 1}, r)

    def test_to_exif_dms(self):
        loc = DegreeFormatFactory.create([78.0, 55.0, 44.33324])
        r = Converter.to_exif('', loc)
        self.assertIsInstance(r, tuple)

    def test_to_custom_gps_timestamp(self):
        r = Converter.to_custom('gps_timestamp', '15:01:01')
        self.assertIsInstance(r.get_source(), tuple)

    def test_illegal_degree(self):
        dic = {'gps_latitude': 'a'}
        self.assertIsNone(Converter.read_from_dict(dic, 'gps_latitude'))

if __name__ == '__main__':
    unittest.main()