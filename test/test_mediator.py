from exif_edit.formats import DegreeFormatFactory
import unittest
import os

from unittest.mock import MagicMock, Mock
from tksheet import Sheet

from exif_edit.mediator import Mediator

class TestMediator(unittest.TestCase):

    def __path(self, name):
        img = 'test/resources/' + name
        return os.path.realpath(img)

    def __train_sheet_for_data(self, data):
        self.sheet.get_total_rows.return_value = len(data)
        self.sheet.get_sheet_data.return_value = data

    def setUp(self):
        self.sheet = Mock(name='sheet', spec=Sheet)
        self.mediator = Mediator(self.sheet)

    def test_add(self):
        self.mediator.add_row()
        self.sheet.insert_row.assert_called_with(redraw=True)

    def test_insert_row(self):
        self.sheet.get_total_rows.return_value = 1
        self.sheet.get_selected_rows.return_value = {0}
        self.mediator.insert_row()
        self.assertTrue(self.mediator.has_rows())
        self.sheet.insert_row.assert_called_with(idx=1, redraw=True)

    def test_insert_row_after_selected_cell(self):
        self.sheet.get_selected_rows.return_value = {}
        self.sheet.get_selected_cells.return_value = {(0,1)}
        self.mediator.insert_row()
        self.sheet.insert_row.assert_called_with(idx=1, redraw=True)

    def test_remove_row_selected_row(self):
        self.sheet.get_selected_rows.return_value = [0]
        self.sheet.get_column_data = Mock(return_value=[[0]])

        self.mediator.remove_row()

        expected_calls = [self.sheet.get_selected_rows, self.sheet.get_column_data,
            self.sheet.get_cell_data, self.sheet.delete_row, self.sheet.refresh]
        self.sheet.mock_calls = expected_calls
        self.sheet.delete_row.assert_called_with(0, True)

    def test_remove_row_selected_cell(self):
        self.sheet.get_selected_rows.return_value = {}
        self.sheet.get_selected_cells.return_value = {(0,1)}
        self.sheet.get_column_data = Mock(return_value=[[0]])

        self.mediator.remove_row()

        expected_calls = [self.sheet.get_selected_rows, self.sheet.get_column_data,
            self.sheet.get_cell_data, self.sheet.delete_row, self.sheet.refresh]
        self.sheet.mock_calls = expected_calls
        self.sheet.delete_row.assert_called_with(0, True)

    def test_append_exif(self):
        self.sheet.get_total_rows =  Mock(side_effect=[1, 0])

        self.mediator.append_exif(self.__path('lookup.jpg'))
        expected_calls = [self.sheet.set_sheet_data(), self.sheet.set_all_column_widths,
            self.sheet.readonly_rows, self.sheet.readonly_cells]
        self.sheet.mock_calls = expected_calls

    def test_save_exif(self):
        self.sheet.get_total_rows.return_value = 0
        self.mediator.append_exif(self.__path('lookup.jpg'))
        self.sheet.get_sheet_data.return_value = [["model", "bar"]]

        self.mediator.save_exif(self.__path('modified.jpg'))

    def test_keep_origin(self):
        self.mediator.begin_edit_cell((0,0))
        self.sheet.get_cell_data.assert_called()

    def test_restore_origin(self):
        self.sheet.get_cell_data = Mock(return_value="exif_version")
        self.sheet.get_column_data = Mock(return_value=["exif_version", "exif_version"])

        self.mediator.begin_edit_cell((0,0))
        self.mediator.end_edit_cell((0,0))
        self.sheet.set_cell_data.assert_called()

    def test_restore_origin_not_whitespace(self):
        self.sheet.get_cell_data = Mock(return_value="")

        self.mediator.end_edit_cell((0,0))
        self.sheet.set_cell_data.assert_not_called()

    def test_parse_location(self):
        self.sheet.get_cell_data = Mock(side_effect=["gps_latitude", "78°55\'44.33324\""])
        self.mediator.end_edit_cell((1,1))
        self.sheet.set_cell_data.assert_called()

    def test_parse_location_restore_origin(self):
        cell = (1,1)
        deg = DegreeFormatFactory.create("78.4")
        self.sheet.get_cell_data = Mock(side_effect=[deg, "gps_latitude", "a"])
        self.mediator.begin_edit_cell(cell)
        self.mediator.end_edit_cell(cell)
        self.sheet.set_cell_data.assert_called_with(cell[0], cell[1], deg)

    def test_get_remove_button_state(self):
        self.sheet.get_selected_rows = Mock(return_value= [0])
        event = ('select_row', (0,))
        self.assertTrue(self.mediator.can_remove_row(event))

    def test_get_remove_button_state_disabled(self):
        event = ('foo', (0,))
        self.assertFalse(self.mediator.can_remove_row(event))

    def test_sort(self):
        data = [["model", "baz"], ["foo", "bar"], ["exif_version", "220"]]
        self.sheet.get_total_rows = Mock(side_effect=[len(data), len(data), 0])
        self.sheet.get_sheet_data.return_value = data
        self.mediator.sort()
        self.sheet.set_sheet_data.assert_called_with(
            [['exif_version', '220'], ['foo', 'bar'], ['model', 'baz']], redraw=True)

    def test_open_location_no_coordinates(self):
        data = [["model", "bar"]]
        self.__train_sheet_for_data(data)
        self.mediator.open_url = MagicMock()
        self.mediator.show_location()
        self.mediator.open_url.assert_not_called()

    def test_open_location_coordinates(self):
        deg = DegreeFormatFactory.create((1,1,1))
        data = [["gps_latitude", deg], ["gps_longitude", deg]]
        self.__train_sheet_for_data(data)
        self.mediator.open_url = MagicMock()
        self.mediator.show_location()
        self.mediator.open_url.assert_called_once()

    def test_has_location(self):
        deg = DegreeFormatFactory.create((1,1,1))
        data = [["gps_latitude", deg], ["gps_longitude", deg]]
        self.__train_sheet_for_data(data)
        self.assertTrue(self.mediator.has_location())

    def test_read_image(self):
        with Mediator.read_image(self.__path('lookup.jpg')) as img:
            self.assertIsNotNone(img)

    def test_read_icon(self):
        with Mediator.read_icon("exit.png") as icon:
            self.assertIsNotNone(icon)

if __name__ == '__main__':
    unittest.main()
