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
        self.sheet = Mock(name='sheet', spec=Sheet)
        self.mediator = Mediator(self.sheet)

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
        self.mediator.add_row()
        
        self.sheet.insert_row.assert_called()
        self.sheet.refresh.assert_called()

    def test_remove_row(self):
        self.sheet.get_selected_rows.return_value = [0]
        self.sheet.get_column_data = Mock(return_value=[[0]])

        self.mediator.remove_row()

        self.sheet.delete_row.assert_called()
        self.sheet.refresh.assert_called()

    def test_append_exif(self):
        self.mediator.append_exif(self.__path('lookup.jpg'))
        self.sheet.set_sheet_data.assert_called()

    def test_save_exif(self):
        self.mediator.append_exif(self.__path('lookup.jpg'))
        self.sheet.get_sheet_data.return_value = [["model", "bar"]]
        
        self.mediator.save_exif(self.__path('modified.jpg'))

    def test_keep_origin(self):
        self.mediator.keep_origin((0,1))
        self.sheet.get_cell_data.assert_called()

    def test_not_keep_origin(self):
        self.mediator.keep_origin((0,0))
        self.sheet.get_cell_data.assert_not_called()

    def test_restore_origin(self):
        self.mediator.restore_origin((0,1))
        self.sheet.set_cell_data.assert_not_called()

if __name__ == '__main__':
    unittest.main()