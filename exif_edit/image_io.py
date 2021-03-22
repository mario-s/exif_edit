"""
IO package to read and write.
"""

from exif import Image as Exif
from PIL import Image
from sortedcontainers import SortedDict

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
        return ("bits_per_sample", "compression",
            "image_height", "image_width", "image_unique_id",
            "jpeg_interchange_format", "jpeg_interchange_format_length",
            "photometric_interpretation",
            "resolution_unit",
            "samples_per_pixel", "x_resolution", "y_resolution")

    @staticmethod
    def read_only():
        """Filter for attributes which are read only."""
        return "_exif_ifd_pointer", "exif_version"


class Reader:

    """This class reads Exif Tags and the image itself."""

    def __init__(self, img_path):
        with open(img_path, 'rb') as file:
            self.image = Exif(file)

    def binary(self):
        return self.image

    @classmethod
    def read_image(cls, img_path, scale=False, max_len=400):
        """
        This method reads the binary image.
        If the parameter scale is True, then the image will be scaled using max_len.
        """
        img = Image.open(img_path)

        if scale:
            img.thumbnail((max_len, max_len))
        
        return img

    def keys(self) -> list[str]:
        return self.image.list_all()

    def value(self, key) -> str:
        return Converter.try_read(self.image, key)

    def dict(self) -> dict:
        lst = []
        for key in self.keys():
            value = self.value(key)
            if not value is None:
                lst.append((key, value))

        return dict(lst)

    def grouped_dict(self) -> dict:
        """Returns a dictionary with groups, were every group is sorted"""
        dic = self.dict()
        #sort elements seperately, which can only be read
        read_only = SortedDict(self.__filter(dic, ExifFilter.read_only()))
        #sort elements seperately, which can not be deleted
        edit_only = SortedDict(self.__filter(dic, ExifFilter.not_deleteable()))
        #join the dictionaries
        return read_only | edit_only | SortedDict(dic)

    @classmethod 
    def __filter(cls, dic, fltr):
        """Remove elements from dictionary to avoid sorting them in the big one"""
        return [(k, dic.pop(k)) for k in fltr if k in dic]


class Writer:
    """This class writes the edited Exif Tags back to the image."""

    def __init__(self, image):
        self.image = image
        self.converter = Converter()

    def save(self, collection, img_path):
        """Saves the the collection of Exif tags to a file given by the path."""
        if isinstance(collection, dict):
            self.__set_values(collection)
        elif isinstance(collection, list):
            self.__set_values(self.__list_to_dict(collection))
        else:
            raise ValueError("Expect either dict or list[list]!")

        self.__save(img_path)

    @classmethod
    def __list_to_dict(cls, row) -> dict:
        dic = {}
        for col in row:
            if len(col) < 2:
                raise ValueError("Expect at least two cells in the row")
            dic[col[0]] = col[1]
        return dic

    def __set_values(self, dic):
        self.__delete_all()
        for key, value in dic.items():
            if key not in ExifFilter.read_only() and value is not None:
                val = self.converter.cast(key, value)
                self.image.set(key, val)

    def __delete_all(self):
        #we need to iterate through each and check if we allowed to delete it,
        #if not we will have problems while saving the new tags
        locked = ExifFilter.locked()
        for key in self.image.list_all():
            if key not in locked:
                self.image.delete(key)
    
    def __save(self, img_path):
        with open(img_path, 'wb') as file:
            file.write(self.image.get_file())
