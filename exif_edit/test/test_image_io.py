import unittest
import os
from unittest.mock import Mock
from tksheet import Sheet

from ..image_io import ExifReader, ExifWriter, ImageReader, Mediator

class TestIO(unittest.TestCase):

    def __path(self, name):
        img = 'exif_edit/test/resources/' + name
        return os.path.realpath(img)

    def setUp(self):
        p = self.__path('lookup.jpg')
        self.reader = ExifReader(p)
        self.writer = ExifWriter(self.reader.binary())
        self.mock = Mock(name='sheet', spec=Sheet)

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

    def test_add_row(self):
        mediator = Mediator(self.mock)
        mediator.add_row()
        self.mock.insert_row.assert_called()

    def test_remove_row(self):
        self.mock.get_selected_rows.return_value = []
        mediator = Mediator(self.mock)
        mediator.remove_row()
        self.mock.get_selected_rows.assert_called()

if __name__ == '__main__':
    unittest.main()