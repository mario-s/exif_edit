from exif_edit.converter import Converter
import unittest
import os

from exif_edit.image_io import ExifFilter, Reader, Writer

class TestImageIO(unittest.TestCase):

    def __path(self, name):
        img = 'test/resources/' + name
        return os.path.realpath(img)

    def setUp(self):
        p = self.__path('lookup.jpg')
        self.reader = Reader(p)
        self.writer = Writer(self.reader.binary())

    def test_keys(self):
        self.assertFalse(len(self.reader.keys()) == 0)

    def test_value(self):
        keys = self.reader.keys()
        val = self.reader.value(keys[0])
        self.assertIsNotNone(val)

    def test_dict(self):
        res = self.reader.dict()
        self.assertFalse(len(res) == 0)

    def test_grouped_dict(self):
        lst = list(self.reader.grouped_dict().keys())
        k = ExifFilter.read_only()[0]
        self.assertEqual(0, lst.index(k))

    def test_save_list(self):
        list = [["model", "bar"]]
        p = self.__path('modified.jpg')
        self.writer.save(list, p)

        keys = Reader(p).keys()
        self.assertTrue("model" in keys)

    def test_save_list_deleted_row(self):
        lst = [["model", "bar"], ["software", "python"]]
        p = self.__path('modified.jpg')
        writer = Writer(self.reader.binary(), Converter.to_dict(lst))
        writer.save([["model", "bar"]], p)

        keys = Reader(p).keys()
        self.assertFalse("software" in keys)

    def test_read_image(self):
        img = Reader.read_image(self.__path('lookup.jpg'), True)
        w, _ = img.size
        self.assertEqual(400, w)

if __name__ == '__main__':
    unittest.main()
