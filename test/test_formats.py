import unittest

from exif_edit.formats import DmsFormat, DecimalFormat, DegreeFormatFactory, TimeStamp

class TestFormats(unittest.TestCase):

    def test_wrong_args(self):
        self.assertRaises(ValueError, lambda: DmsFormat([1]))
        self.assertRaises(ValueError, lambda: DecimalFormat(None))
        self.assertRaises(ValueError, lambda: DegreeFormatFactory.create("a"))
        self.assertRaises(ValueError, lambda: TimeStamp.parse([1]))

    def test_factory_format_arg(self):
        loc = DmsFormat((78, 55, 44.33324))
        self.assertEqual(loc, DegreeFormatFactory.create(loc))

    def test_dms_to_dd_tuple(self):
        loc = DegreeFormatFactory.create((78, 55, 44.33324))
        self.assertEqual(78.928981, loc.as_float())

    def test_dms_to_dd_list(self):
        loc = DegreeFormatFactory.create([-78, 55, 44.33324])
        self.assertEqual(-78.928981, loc.as_float())

    def test_dms_to_string(self):
        loc = DegreeFormatFactory.create([78.0, 55.0, 44.33324])
        self.assertEqual("78°55\'44.33324\"", loc.__repr__())

    def test_dec_to_dms(self):
        loc = DegreeFormatFactory.create(30.263888889)
        self.assertEqual((30, 15, 50), loc.as_tuple())

    def test_dec_to_string(self):
        loc = DegreeFormatFactory.create(30.263888889)
        self.assertEqual("30.263889°", loc.__repr__())

    def test_parse_to_dms(self):
        loc = DegreeFormatFactory.create("78°55\'44.33324\"")
        self.assertEqual(78.928981, loc.as_float())

    def test_parse_to_dec(self):
        loc = DegreeFormatFactory.create("30.263888889°")
        self.assertEqual((30, 15, 50), loc.as_tuple())

    def test_parser_raises_error(self):
        self.assertRaises(ValueError, lambda: DegreeFormatFactory.parse('4711a'))

    def test_timestamp_parse_tuple(self):
        tpl = (15,0,1)
        tmt = TimeStamp.parse(tpl)
        self.assertEqual("15:00:01", tmt.__repr__())
        self.assertEqual(tpl, tmt.get_source())

    def test_timestamp_parse_string(self):
        tmt = TimeStamp.parse("15:00:01")
        self.assertEqual("15:00:01", tmt.__repr__())

if __name__ == '__main__':
    unittest.main()