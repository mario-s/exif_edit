import unittest
import os
import tkinter as tk
from unittest.mock import MagicMock, Mock
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
        
        expected_calls = [self.sheet.insert_row, self.sheet.refresh]
        self.sheet.mock_calls = expected_calls

    def test_remove_row(self):
        self.sheet.get_selected_rows.return_value = [0]
        self.sheet.get_column_data = Mock(return_value=[[0]])

        self.mediator.remove_row()

        expected_calls = [self.sheet.get_selected_rows, self.sheet.get_column_data,
            self.sheet.get_cell_data, self.sheet.delete_row, self.sheet.refresh]
        self.sheet.mock_calls = expected_calls

    def test_append_exif(self):
        self.mediator.append_exif(self.__path('lookup.jpg'))
        expected_calls = [self.sheet.set_sheet_data(), self.sheet.set_all_column_widths, 
            self.sheet.readonly_rows, self.sheet.readonly_cells]
        self.sheet.mock_calls = expected_calls

    def test_save_exif(self):
        self.mediator.append_exif(self.__path('lookup.jpg'))
        self.sheet.get_sheet_data.return_value = [["model", "bar"]]
        
        self.mediator.save_exif(self.__path('modified.jpg'))

    def test_keep_origin(self):
        self.mediator.keep_origin((0,0))
        self.sheet.get_cell_data.assert_called()

    def test_restore_origin(self):
        self.sheet.get_cell_data = Mock(return_value="exif_version")
        self.sheet.get_column_data = Mock(return_value=["exif_version", "exif_version"])

        self.mediator.keep_origin((0,0))
        self.mediator.restore_origin((0,0))
        self.sheet.set_cell_data.assert_called()

    def test_restore_origin_not_whitespace(self):
        self.sheet.get_cell_data = Mock(return_value="")

        self.mediator.restore_origin((0,0))
        self.sheet.set_cell_data.assert_not_called()

    def test_get_remove_button_state(self):
        self.sheet.get_selected_rows = Mock(return_value= [0])
        event = ('select_row', (0,))
        self.assertEqual(tk.NORMAL, self.mediator.get_remove_button_state(event))

    def test_get_remove_button_state_disabled(self):
        event = ('foo', (0,))
        self.assertEqual(tk.DISABLED, self.mediator.get_remove_button_state(event))

    def test_open_location_no_coordinates(self):
        self.sheet.get_sheet_data.return_value = [["model", "bar"]]
        self.mediator.open_url = MagicMock()
        self.mediator.open_location()
        self.mediator.open_url.assert_not_called


if __name__ == '__main__':
    unittest.main()