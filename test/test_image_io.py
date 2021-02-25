import unittest
import os
from exif import ColorSpace, ResolutionUnit

from exif_edit.image_io import ExifReader, ExifWriter, ImageReader, Converter

class TestImageIO(unittest.TestCase):

    def __path(self, name):
        img = 'test/resources/' + name
        return os.path.realpath(img)

    def setUp(self):
        p = self.__path('lookup.jpg')
        self.reader = ExifReader(p)
        self.writer = ExifWriter(self.reader.binary())

    def test_keys(self):
        self.assertFalse(len(self.reader.keys()) == 0)

    def test_value(self):
        k = self.reader.keys()
        v = self.reader.value(k[0])
        self.assertIsNotNone(v)

    def test_dict(self):
        d = self.reader.dict()
        self.assertFalse(len(d) == 0)

    def test_list(self):
        l = self.reader.list_of_lists()
        self.assertFalse(len(l) == 0)

    def test_save_dict(self):
        dict = {"model": "bar"}
        p = self.__path('modified.jpg')
        self.writer.save(dict, p)

        keys = ExifReader(p).keys()
        first_key = next(iter(dict))
        self.assertTrue(first_key in keys)

    def test_save_list(self):
        list = [["model", "bar"]]
        p = self.__path('modified.jpg')
        self.writer.save(list, p)

        keys = ExifReader(p).keys()
        self.assertTrue("model" in keys)

    def test_read_image(self):
        i = ImageReader.read(self.__path('lookup.jpg'))
        w, _ = i.size
        self.assertEqual(400, w)

    def test_converter_unknown(self):
        self.assertEqual(1, Converter.convert('foo', 1))

    def test_converter_color_space_srgb(self):
        self.assertEqual(ColorSpace.SRGB, Converter.convert("color_space", "1"))

    def test_converter_color_space_uncalibrated(self):
        self.assertEqual(ColorSpace.UNCALIBRATED, Converter.convert("color_space", "0"))

    def test_converter_resolution_unit_centimeters(self):
        self.assertEqual(ResolutionUnit.CENTIMETERS, Converter.convert("resolution_unit", "3"))

    def test_converter_resolution_unit_inches(self):
        self.assertEqual(ResolutionUnit.INCHES, Converter.convert("resolution_unit", "1"))
    

if __name__ == '__main__':
    unittest.main()