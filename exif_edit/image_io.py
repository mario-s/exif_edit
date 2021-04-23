"""
IO package to read and write.
"""

from exif import Image as Exif
from PIL import Image

from exif_edit.converter import Converter, ExifFilter

class Reader:
    """This class reads Exif Tags and the image itself."""

    def __init__(self, img_path):
        with open(img_path, 'rb') as file:
            self.image = Exif(file)

    def binary(self):
        """
        This method returns the binary object, which is the image itself.
        """
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
        """
        This method returns a list of all keys, present in the Exif data.
        """
        return self.image.list_all()

    def value(self, key) -> str:
        """
        This method returns the value for a given key.
        """
        return Converter.read_from_dict(self.image, key)

    def dict(self) -> dict:
        """
        This method returns a dictionary of all the exif data.
        """
        lst = []
        for key in self.keys():
            value = self.value(key)
            if not value is None:
                lst.append((key, value))

        return dict(lst)

    def grouped_dict(self) -> dict:
        """
        Returns a dictionary with groups, where every group is sorted.
        """
        return Converter.group_dict(self.dict())


class Writer:
    """This class writes the edited Exif Tags back to the image."""

    def __init__(self, image):
        self.image = image
        self.converter = Converter()

    def save(self, rows, img_path):
        """
        Saves the the collection of Exif tags to a file given by the path.
        """
        self.__set_values(Converter.rows_to_dict(rows))
        self.__save(img_path)

    def __set_values(self, dic):
        self.__delete_all()
        for key, value in dic.items():
            if key not in ExifFilter.read_only() and value is not None:
                try:
                    val = self.converter.to_exif(key, value)
                    #print(f"{key}, {val}")
                    self.image[key] = val
                except Exception as e:
                    print(e)


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
