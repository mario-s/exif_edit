from PIL import ImageTk
from exif_edit.image_io import ImageReader, ExifReader, ExifWriter

class Mediator:
    def __init__(self, sheet):
        self.sheet = sheet

    def append_exif(self, img_path):
        reader = ExifReader(img_path)
        lists = reader.list_of_lists()
        self.sheet.set_sheet_data(lists)
        self.__disable_rows__(lists)
        self.sheet.set_all_column_widths(250)
        self.origin_img_path = img_path

    def __disable_rows__(self, lists):
        rows = []
        for i in range(len(lists)):
            list = lists[i]
            if list[0] in ExifWriter.filter():
                rows.append(i)
        self.sheet.readonly_rows(rows)

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
            if row < total_rows:
                self.sheet.delete_row(row)
                index+=1

        self.sheet.refresh()

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
            if key in ExifWriter.filter():
                value = self.origin_cell_value
                self.sheet.set_cell_data(r, 1, value)

    def __is_in_value_column(self, row):
        return row[1] == 1