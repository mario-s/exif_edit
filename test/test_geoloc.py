import unittest

from exif_edit.geoloc import DmsFormat

class TestDmsFormat(unittest.TestCase):

    def test_wrong_constructor_arg(self):
        self.assertRaises(ValueError, lambda: DmsFormat([1]))

    def test_dms_to_dd_tuple(self):
        loc = DmsFormat((78, 55, 44.33324))
        self.assertEqual(78.928981, loc.decimalDegrees())

    def test_dms_to_dd_list(self):
        loc = DmsFormat([78, 55, 44.33324])
        self.assertEqual(78.928981, loc.decimalDegrees())

    def test_to_string(self):
        loc = DmsFormat([78.0, 55.0, 44.33324])
        self.assertEquals("78°55\'44.33324\"", loc.__repr__())


if __name__ == '__main__':
    unittest.main()