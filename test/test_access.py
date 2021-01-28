import unittest
import os
from exif_edit.access import Reader, Writer

class TestReader(unittest.TestCase):

    def path(self, name):
        img = 'test/resources/' + name
        return os.path.realpath(img)

    def setUp(self):
        p = self.path('lookup.jpg')
        self.reader = Reader(p)
        self.writer = Writer(self.reader.binary())

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
        p = self.path('modified.jpg')
        self.writer.save(dict, p)

        keys = Reader(p).keys()
        first_key = next(iter(dict))
        self.assertTrue(first_key in keys)

    def test_save_list(self):
        list = [["model", "bar"]]
        p = self.path('modified.jpg')
        self.writer.save(list, p)

        keys = Reader(p).keys()
        self.assertTrue("model" in keys)

if __name__ == '__main__':
    unittest.main()