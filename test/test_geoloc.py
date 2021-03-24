import unittest

from exif_edit.geoloc import Degree

class TestLocationFormat(unittest.TestCase):

    def test_dms_to_dd_tuple(self):
        loc = Degree((78, 55, 44.33324))
        self.assertEqual(78.928981, loc.decimalDegrees())

    def test_dms_to_dd_list(self):
        loc = Degree([78, 55, 44.33324])
        self.assertEqual(78.928981, loc.decimalDegrees())

    def test_dd(self):
        loc = Degree(78.92898123)
        self.assertEqual(78.928981, loc.decimalDegrees())


if __name__ == '__main__':
    unittest.main()