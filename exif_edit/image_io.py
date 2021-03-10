from enum import Enum
from sortedcontainers import SortedDict
from exif import Image as Exif
from PIL import Image

from exif_edit.converter import Converter

class ExifFilter:

    """Filter for keys which should be handled different."""

    @staticmethod
    def locked():
        """This method joins all filter into one."""
        return ExifFilter.not_deleteable() + ExifFilter.read_only()

    @staticmethod
    def not_deleteable():
        """Filter for attributes which are editable bot not deletable."""
        return ("image_height", "image_width", "resolution_unit",
            "samples_per_pixel", "x_resolution", "y_resolution")

    @staticmethod
    def read_only():
        """Filter for attributes which are read only."""
        return ("_exif_ifd_pointer", "bits_per_sample",
            "compression", "exif_version",
            "image_unique_id",
            "jpeg_interchange_format", "jpeg_interchange_format_length",
            "photometric_interpretation")


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
        #sort elements seperately, which can not be deleted
        read_only = SortedDict(self.__filter(dic, ExifFilter.read_only()))
        not_editable = SortedDict(self.__filter(dic, ExifFilter.not_deleteable()))
        #join the dictionaries
        return read_only | not_editable | SortedDict(dic)

    def __filter(self, dic, filter):
        """Remove elements from dictionary to avoid sorting them in the big one"""
        return dict([(k, dic.pop(k)) for k in filter if k in dic])

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

    def __list_to_dict(self, row) -> dict:
        dict = {}
        for col in row:
            if len(col) < 2:
                raise ValueError("Expect at least two cells in the row")
            dict[col[0]] = col[1]
        return dict

    def __set_values(self, dict):
        self.__delete_all()
        for key, value in dict.items():
            if key not in ExifFilter.read_only() and value is not None:
                v = self.converter.cast(key, value)
                self.image.set(key, v)

    def __delete_all(self):
        #we need to iterate through each and check if we allowed to delete it,
        #if not we will have problems while saving the new tags
        filter = ExifFilter.locked()
        for key in self.image.list_all():
            if key not in filter:
                self.image.delete(key)
    
    def __save(self, img_path):
        with open(img_path, 'wb') as f:
            f.write(self.image.get_file())

