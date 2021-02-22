from exif import Image as Exif
from PIL import Image, ImageTk

class ImageReader:
    
    @staticmethod
    def read(img_path, base_width=400):
        img = Image.open(img_path)
        img.thumbnail((base_width, base_width))
        return img

class ExifReader:
    def __init__(self, img_path):
        self.filter = ["_exif_ifd_pointer", "exif_version"]
        with open(img_path, 'rb') as f:
            self.image = Exif(f)

    def binary(self):
        return self.image

    def keys(self) -> list[str]:
        return dir(self.image)

    def value(self, key) -> str:
        return self.image.get(key)

    def dict(self) -> dict:
        map = {}
        keys = self.keys()
        for k in keys:
            if self.__is_editable(k):
                v = self.value(k)
                map[k] = v
        return map

    #if not in filter, we can edit it
    def __is_editable(self, key):
        return key not in self.filter

    def list_of_lists(self) -> list[list[str]]:
        return list(map(list, self.dict().items()))


class ExifWriter:
    def __init__(self, image):
        self.image = image

    def save(self, collection, img_path):
        if type(collection) is dict:
            self.__set_values(collection)
        elif type(collection) is list:
            d = self.__list_to_dict(collection)
            self.__set_values(d)
        else:
            raise ValueError("Expect either dict or list[list]!")

        self.__save(img_path)

    def __list_to_dict(self, list) -> dict:
        dict = {}
        for l in list:
            if len(l) < 2:
                raise ValueError("Expect at least two elements in the list")
            dict[l[0]] = l[1]
        return dict

    def __set_values(self, dict):
        for k,v in dict.items():
            if v is not None:
                self.image.set(k, v)
    
    def __save(self, img_path):
        with open(img_path, 'wb') as f:
            f.write(self.image.get_file())


class Mediator:
    def __init__(self, sheet):
        self.sheet = sheet

    def append_exif(self, img_path):
        reader = ExifReader(img_path)
        self.sheet.set_sheet_data(reader.list_of_lists())
        self.sheet.set_all_column_widths(250)
        self.origin_img_path = img_path

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