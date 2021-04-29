import unittest

from exif_edit.location import Coordinate

class TestLocation(unittest.TestCase):

    def setUp(self):
        self.coord = Coordinate(30.263888889, 30.263888889)

    def test_coordinate_to_dec_positive(self):
        self.assertEqual((30.263889, 30.263889), self.coord.decimal())

    def test_coordinate_to_dec_negative(self):
        coord = Coordinate(30.263888889, "30.263888889", lat_ref='S', lon_ref='W')
        self.assertEqual((-30.263889, -30.263889), coord.decimal())

    def test_coordinate_google_maps_url(self):
        expected = 'https://www.google.com/maps/place/30.263889+30.263889/@30.263889,30.263889,10z'
        self.assertEqual(expected, self.coord.google_maps_url())

if __name__ == '__main__':
    unittest.main()
