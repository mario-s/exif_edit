import unittest

from exif_edit.geoloc import LocationFormat

class TestLocationFormat(unittest.TestCase):

    def test_dms_to_dd(self):
        loc = LocationFormat((78, 55, 44.33324))
        self.assertEqual(78.928981, loc.decimalDegrees())


if __name__ == '__main__':
    unittest.main()