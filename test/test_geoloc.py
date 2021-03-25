import unittest

from exif_edit.geoloc import DmsFormat, DecimalFormat

class TestDmsFormat(unittest.TestCase):

    def test_wrong_constructor_arg(self):
        self.assertRaises(ValueError, lambda: DmsFormat([1]))
        self.assertRaises(ValueError, lambda: DecimalFormat(None))

    def test_dms_to_dd_tuple(self):
        loc = DmsFormat((78, 55, 44.33324))
        self.assertEqual(78.928981, loc.decimalDegrees())

    def test_dms_to_dd_list(self):
        loc = DmsFormat([78, 55, 44.33324])
        self.assertEqual(78.928981, loc.decimalDegrees())

    def test_dms_to_string(self):
        loc = DmsFormat([78.0, 55.0, 44.33324])
        self.assertEquals("78°55\'44.33324\"", loc.__repr__())

    def test_dec_to_dms(self):
        loc = DecimalFormat(30.263888889)
        self.assertEquals((30, 15, 50), loc.dmsDegrees())

    def test_dec_to_string(self):
        loc = DecimalFormat(30.263888889)
        self.assertEquals("30.263889°", loc.__repr__())


if __name__ == '__main__':
    unittest.main()