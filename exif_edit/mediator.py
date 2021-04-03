"""
Mediator to coordinate tasks.
"""

import os
import logging
import webbrowser

from typing import Optional

from exif_edit.image_io import ExifFilter, Reader, Writer
from exif_edit.converter import Converter
from exif_edit.geoloc import Coordinate, Factory

class Mediator:

    """This mediator coordinates between the GUI and the reading/ writing of the image."""

    def __init__(self, sheet):
        self.sheet = sheet

    def append_exif(self, img_path):
        reader = Reader(img_path)
        dic = reader.grouped_dict()

        self.origin_img_path = img_path
        self.sheet.set_sheet_data(self.__to_list(dic))
        self.__disable_rows(dic)

    @classmethod
    def __to_list(cls, dic) -> list[list[str]]:
        return list(map(list, dic.items()))

    def __disable_rows(self, dic):
        keys = list(dic.keys())

        rows = self.__count_matching_rows(keys, ExifFilter.read_only())
        if len(rows) > 0:
            self.sheet.readonly_rows(rows)
            self.sheet.highlight_rows(rows, bg = "light blue", fg = "black")

        rows = self.__count_matching_rows(keys, ExifFilter.not_deleteable())
        if len(rows) > 0:
            for row in rows:
                self.sheet.readonly_cells(row, 0)
            self.sheet.highlight_rows(rows, bg = "light green", fg = "black")

    @classmethod
    def __count_matching_rows(cls, keys, fltr):
        return [i for i in range(len(keys)) if keys[i] in fltr]

    @classmethod
    def read_image(cls, img_path):
        return Reader.read_image(img_path, True)

    @classmethod
    def read_icon(cls, icon_name):
        icon_path = os.path.join(os.path.dirname(__file__), "assets/" + icon_name)
        return Reader.read_image(icon_path)

    def add_row(self):
        self.sheet.insert_row()
        self.sheet.refresh()

    def remove_row(self):
        index = 0
        selected_rows = self.sheet.get_selected_rows()
        for selected in selected_rows:
            col_data = self.sheet.get_column_data(0)
            total_rows = len(col_data)
            row = selected - index
            if row < total_rows and self.__is_deletable(row):
                self.sheet.delete_row(row)
                index+=1

        self.sheet.refresh()

    def can_remove_row(self, event) -> bool:
        name = event[0]
        if name in ("select_row", "drag_select_rows"):
            return True if self.__is_editable_row_selected() else False
        return False

    def __is_editable_row_selected(self):
        selected_rows = self.sheet.get_selected_rows()
        return [self.__is_deletable(row) for row in selected_rows].count(True) > 0

    def __is_deletable(self, row):
        key = self.sheet.get_cell_data(row, 0)
        return not key in ExifFilter.locked()

    def save_exif(self, new_img_path="", origin_img_path=""):
        orig_path = self.__path(self.origin_img_path, origin_img_path)
        img = Reader(orig_path).binary()
        writer = Writer(img)

        target_path = self.__path(orig_path, new_img_path)
        logging.info("saving file: %s", target_path)
        data = self.sheet.get_sheet_data()
        writer.save(data, target_path)

    @classmethod
    def __path(cls, source, path):
        return source if (path is None or path == "") else path

    def begin_edit_cell(self, cell):
        """Listener for begin of cell edit."""
        orig = self.sheet.get_cell_data(cell[0], cell[1])
        self.origin_cell_value = orig

    def end_edit_cell(self, cell):
        """
        Listener for end edit of a cell.
        """
        if self.__is_location_value(cell):
            self.__parse_location(cell)
        else:
            self.__restore_origin_key(cell)

    def __is_location_value(self, cell):
        if not self.__is_in_key_column(cell):
            key = self.sheet.get_cell_data(cell[0], 0)
            return Converter.is_geoloc(key)
        return False

    def __parse_location(self, cell):
        dat = self.sheet.get_cell_data(cell[0], cell[1])
        try:
            deg = Factory.create(dat)
            self.sheet.set_cell_data(cell[0], cell[1], deg, False, True)
        except ValueError as exc:
            logging.warning(exc)
            self.__restore_origin_cell_data(cell[0], cell[1])

    def __restore_origin_key(self, cell):
        """
            Restores the original cell data in the key column.
        """
        if self.__is_in_key_column(cell):
            row = cell[0]
            #only one unique value is allowed
            if self.__has_duplicate_keys(row):
                origin = self.origin_cell_value
                self.__restore_origin_cell_data(row, 0)

    def __restore_origin_cell_data(self, row, column):
        origin = self.origin_cell_value
        self.sheet.set_cell_data(row, column, origin)

    @classmethod
    def __is_in_key_column(cls, cell):
        return cell[1] == 0

    def __has_duplicate_keys(self, row):
        key = self.sheet.get_cell_data(row, 0)
        if "".__eq__(key):
            return False
        keys = self.sheet.get_column_data(0)
        return keys.count(key) > 1

    def has_location(self) -> bool:
        """
        This method returns True is there is a location info in the data,
        else False.
        """
        return not self.find_location() is None

    def show_location(self):
        """
        This method shows a location, if it is present, in the default browser.
        """
        loc = self.find_location()
        if not loc is None:
            url = self.__maps_url(loc)
            self.open_url(url)

    def find_location(self) -> Optional[Coordinate]:
        """
        This method looks for a possible coordinate in the Exif data.
        If there is one it will return it, if there is none it will return None.
        """
        data = self.sheet.get_sheet_data()
        dic = Converter.rows_to_dict(data)
        loc = (dic.get('gps_latitude'), dic.get('gps_longitude'))
        if all(loc):
            la_ref = dic.get('gps_latitude_ref')
            lo_ref = dic.get('gps_longitude_ref')
            return Coordinate(loc[0], loc[1], lat_ref=la_ref, lon_ref=lo_ref)
        return None

    @classmethod
    def __maps_url(cls, loc):
        lat, lon = loc.decimal()
        return f"https://www.google.com/maps/place/{lat}+{lon}/@{lat},{lon},10z"

    @classmethod
    def open_url(cls, url):
        """
        Opens the given URL in the systems's default browser.
        """
        webbrowser.open(url, new=0)
