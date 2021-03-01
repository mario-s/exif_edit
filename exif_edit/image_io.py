from enum import Enum
from sortedcontainers import SortedDict
from exif import Image as Exif
from PIL import Image

from exif_edit.converter import Converter

class ExifFilter:

    @staticmethod
    def filter():
        return "exif_version",

class ImageReader:
    
    """This class reads the binary image, which will be used to display in the GUI."""

    @staticmethod
    def read(img_path, base_width=400):
        img = Image.open(img_path)
        img.thumbnail((base_width, base_width))
        return img

class ExifReader:

    """This class reads all Exif Tags from the image."""

    def __init__(self, img_path):
        self.filter = ("exif_version")
        with open(img_path, 'rb') as f:
            self.image = Exif(f)

    def binary(self):
        return self.image

    def keys(self) -> list[str]:
        return self.image.list_all()

    def value(self, key) -> str:
        v = self.image.get(key)
        #human readable value if we have an enum
        if isinstance(v, Enum):
            return v.name
        return v

    def dict(self) -> dict:
        list = [(key, self.value(key)) for key in self.keys()]
        return dict(list)

    def grouped_dict(self) -> dict:
        dic = self.dict()
        #remove elements from dictionary to avoid sorting them in the big one
        list = [(k, dic.pop(k)) for k in ExifFilter.filter() if k in dic]
        #sort those elements seperately
        head = SortedDict(dict(list))
        #join the dictionaries
        return head | SortedDict(dic)

class ExifWriter:

    """This class writes the edited Exif Tags back to the image."""

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
            if key not in ExifFilter.filter() and value is not None:
                v = self.converter.to_enumeration(key, value)
                self.image.set(key, v)
    
    def __save(self, img_path):
        with open(img_path, 'wb') as f:
            f.write(self.image.get_file())

