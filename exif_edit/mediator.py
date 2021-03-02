from PIL import ImageTk
from tkinter import NORMAL, DISABLED 
from exif_edit.image_io import ImageReader, ExifFilter, ExifReader, ExifWriter

class Mediator:

    """This mediator coordinates between the GUI and the reading/ writing of the image."""

    def __init__(self, sheet):
        self.sheet = sheet

    def append_exif(self, img_path):
        reader = ExifReader(img_path)
        dict = reader.grouped_dict()

        self.origin_img_path = img_path
        self.sheet.set_sheet_data(self.__to_list(dict))
        self.sheet.set_all_column_widths(230)
        self.__disable_rows(dict)

    def __to_list(self, dict) -> list[list[str]]:
        return list(map(list, dict.items()))

    def __disable_rows(self, dict):
        rows = []
        keys = list(dict.keys())
        for i in range(len(keys)):
            if keys[i] in ExifFilter.filter():
                rows.append(i)
        if len(rows) > 0:
            self.sheet.readonly_rows(rows)
            self.sheet.highlight_rows(rows, bg = "light blue", fg = "black")

    def read_image(self, img_path):
        return ImageTk.PhotoImage(ImageReader.read(img_path))

    def add_row(self):
        self.sheet.insert_row()
        self.sheet.refresh()

    def remove_row(self):
        index = 0
        selected_rows = self.sheet.get_selected_rows()
        for next in selected_rows:
            col_data = self.sheet.get_column_data(0)
            total_rows = len(col_data)
            row = next - index
            if row < total_rows and self.__is_editable(row):
                self.sheet.delete_row(row)
                index+=1

        self.sheet.refresh()

    def get_remove_button_state(self, event):
        name = event[0]
        if name == "select_row" or "drag_select_rows":
            return NORMAL if self.__is_editable_row_selected() else DISABLED
        return DISABLED

    def __is_editable_row_selected(self):
        selected_rows = self.sheet.get_selected_rows()
        return [self.__is_editable(row) for row in selected_rows].count(True) > 0

    def __is_editable(self, row):
        key = self.sheet.get_cell_data(row, 0)
        return not key in ExifFilter.filter()

    def save_exif(self, new_img_path="", origin_img_path=""):
        orig_path = self.__path(self.origin_img_path, origin_img_path)
        img = ExifReader(orig_path).binary()
        writer = ExifWriter(img)

        target_path = self.__path(orig_path, new_img_path)
        data = self.sheet.get_sheet_data()
        writer.save(data, target_path)

    def __path(self, source, path):
        return source if (path is None or path == "") else path

    def keep_origin(self, row):
        if self.__is_in_value_column(row):
            value = self.sheet.get_cell_data(row[0], 1)
            self.origin_cell_value = value

    def restore_origin(self, row):
        if self.__is_in_value_column(row):
            r = row[0]
            key = self.sheet.get_cell_data(r, 0)
            print(key)
            if key in ExifFilter.filter():
                value = self.origin_cell_value
                self.sheet.set_cell_data(r, 1, value)

    def __is_in_value_column(self, row):
        return row[1] == 1