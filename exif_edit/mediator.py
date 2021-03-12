from tkinter import DISABLED, NORMAL

from PIL import ImageTk

from exif_edit.image_io import ExifFilter, ExifReader, ExifWriter, ImageReader


class Mediator:

    """This mediator coordinates between the GUI and the reading/ writing of the image."""

    def __init__(self, sheet):
        self.sheet = sheet

    def append_exif(self, img_path):
        reader = ExifReader(img_path)
        dic = reader.grouped_dict()

        self.origin_img_path = img_path
        self.sheet.set_sheet_data(self.__to_list(dic))
        self.sheet.set_all_column_widths(230)
        self.__disable_rows(dic)

    def __to_list(self, dic) -> list[list[str]]:
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

    def __count_matching_rows(self, keys, fltr):
        return [i for i in range(len(keys)) if keys[i] in fltr]

    def read_image(self, img_path):
        return ImageTk.PhotoImage(ImageReader.read(img_path))

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

    def get_remove_button_state(self, event):
        name = event[0]
        if name == "select_row" or name == "drag_select_rows":
            return NORMAL if self.__is_editable_row_selected() else DISABLED
        return DISABLED

    def __is_editable_row_selected(self):
        selected_rows = self.sheet.get_selected_rows()
        return [self.__is_deletable(row) for row in selected_rows].count(True) > 0

    def __is_deletable(self, row):
        key = self.sheet.get_cell_data(row, 0)
        return not key in ExifFilter.locked()

    def save_exif(self, new_img_path="", origin_img_path=""):
        orig_path = self.__path(self.origin_img_path, origin_img_path)
        img = ExifReader(orig_path).binary()
        writer = ExifWriter(img)

        target_path = self.__path(orig_path, new_img_path)
        data = self.sheet.get_sheet_data()
        writer.save(data, target_path)

    def __path(self, source, path):
        return source if (path is None or path == "") else path

    def keep_origin(self, cell):
        """Keep the original value of the cell."""
        orig = self.sheet.get_cell_data(cell[0], cell[1])
        self.origin_cell_value = orig

    def restore_origin(self, cell):
        """ 
            Restores the original value. 
            In case of the key column it means avoiding duplicates.
        """
        if self.__is_in_key_column(cell):
            row = cell[0]
            #only one unique value is allowed
            if self.__has_duplicate_keys(row):
                origin = self.origin_cell_value
                self.sheet.set_cell_data(row, 0, origin)

    def __is_in_key_column(self, cell):
        return cell[1] == 0

    def __has_duplicate_keys(self, row):
        key = self.sheet.get_cell_data(row, 0)
        if "".__eq__(key):
            return False
        keys = self.sheet.get_column_data(0)
        return keys.count(key) > 1