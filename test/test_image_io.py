import unittest
import os

from exif_edit.image_io import ExifFilter, ExifReader, ExifWriter

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
    
    def test_grouped_dict(self):
        l = list(self.reader.grouped_dict().keys())
        k = ExifFilter.read_only()[0]
        self.assertEqual(0, l.index(k))

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
        i = ExifReader.read_thumbnail(self.__path('lookup.jpg'))
        w, _ = i.size
        self.assertEqual(400, w)

if __name__ == '__main__':
    unittest.main()