import unittest

from exif_edit.location import Coordinate

class TestLocation(unittest.TestCase):

    def test_coordinate_to_dec_positive(self):
        coord = Coordinate(30.263888889, 30.263888889)
        self.assertEqual((30.263889, 30.263889), coord.decimal())

    def test_coordinate_to_dec_negative(self):
        coord = Coordinate(30.263888889, "30.263888889", lat_ref='S', lon_ref='W')
        self.assertEqual((-30.263889, -30.263889), coord.decimal())

if __name__ == '__main__':
    unittest.main()