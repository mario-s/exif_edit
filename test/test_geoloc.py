from tkinter.constants import NONE
import unittest

from exif_edit.geoloc import DmsFormat, DecimalFormat, Factory, Coordinate

class TestGeoLoc(unittest.TestCase):

    def test_wrong_args(self):
        self.assertRaises(ValueError, lambda: DmsFormat([1]))
        self.assertRaises(ValueError, lambda: DecimalFormat(None))
        self.assertRaises(ValueError, lambda: Factory.create("a"))

    def test_factory_format_arg(self):
        loc = DmsFormat((78, 55, 44.33324))
        self.assertEqual(loc, Factory.create(loc))

    def test_dms_to_dd_tuple(self):
        loc = Factory.create((78, 55, 44.33324))
        self.assertEqual(78.928981, loc.decimal_degrees())

    def test_dms_to_dd_list(self):
        loc = Factory.create([-78, 55, 44.33324])
        self.assertEqual(-78.928981, loc.decimal_degrees())

    def test_dms_to_string(self):
        loc = Factory.create([78.0, 55.0, 44.33324])
        self.assertEqual("78°55\'44.33324\"", loc.__repr__())

    def test_dec_to_dms(self):
        loc = Factory.create(30.263888889)
        self.assertEqual((30, 15, 50), loc.dms_degrees())

    def test_dec_to_string(self):
        loc = Factory.create(30.263888889)
        self.assertEqual("30.263889°", loc.__repr__())

    def test_parse_to_dms(self):
        loc = Factory.create("78°55\'44.33324\"")
        self.assertEqual(78.928981, loc.decimal_degrees())

    def test_parse_to_dec(self):
        loc = Factory.create("30.263888889°")
        self.assertEqual((30, 15, 50), loc.dms_degrees())

    def test_parser_raises_error(self):
        self.assertRaises(ValueError, lambda: Factory.parse('4711a'))

    def test_coordinate_to_dec_positive(self):
        coord = Coordinate(30.263888889, 30.263888889)
        self.assertEqual((30.263889, 30.263889), coord.decimal())

    def test_coordinate_to_dec_negative(self):
        coord = Coordinate(30.263888889, "30.263888889", lat_ref='S', lon_ref='W')
        self.assertEqual((-30.263889, -30.263889), coord.decimal())


if __name__ == '__main__':
    unittest.main()