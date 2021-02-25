from exif import Image as Exif
from PIL import Image

from exif_edit.converter import Converter

class ImageReader:
    
    @staticmethod
    def read(img_path, base_width=400):
        img = Image.open(img_path)
        img.thumbnail((base_width, base_width))
        return img

class ExifTagsFilter:
    def __init__(self):
        #TODO add converters
        self.tags = ("_exif_ifd_pointer", "exif_version", "bits_per_sample",
            "x_resolution", "y_resolution",
            "image_width", "image_height", "compression",
            "photometric_interpretation", "samples_per_pixel",
            "jpeg_interchange_format", "jpeg_interchange_format_length",
            "pixel_x_dimension", "pixel_y_dimension", 
            "image_unique_id")

    #if not in filter, we can edit it
    def is_editable(self, key):
        return key not in self.tags


class ExifReader:
    def __init__(self, img_path):
        self.filter = ExifTagsFilter()
        with open(img_path, 'rb') as f:
            self.image = Exif(f)

    def binary(self):
        return self.image

    def keys(self) -> list[str]:
        return self.image.list_all()

    def value(self, key) -> str:
        return self.image.get(key)

    def dict(self) -> dict:
        map = {}
        keys = self.keys()
        #print(f"exif keys: {keys}")
        for key in keys:
            if self.filter.is_editable(key):
                v = self.value(key)
                map[key] = v
        return map

    def list_of_lists(self) -> list[list[str]]:
        return list(map(list, self.dict().items()))


class ExifWriter:
    def __init__(self, image):
        self.image = image
        self.converter = Converter()

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
        #todo: add, remove and update
        #self.image.delete_all()
        for key, value in dict.items():
            if value is not None:
                v = self.converter.convert(key, value)
                self.image.set(key, v)
    
    def __save(self, img_path):
        with open(img_path, 'wb') as f:
            f.write(self.image.get_file())
