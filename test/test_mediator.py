import unittest
import os
from unittest.mock import Mock
from tksheet import Sheet

from exif_edit.mediator import Mediator

class TestMediator(unittest.TestCase):

    def __path(self, name):
        img = 'test/resources/' + name
        return os.path.realpath(img)

    def setUp(self):
        self.sheet = Mock(name='sheet', spec=Sheet)
        self.mediator = Mediator(self.sheet)

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