from exif import Image as Exif
from PIL import Image


class ExifReader:
    def __init__(self, img_path):
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
            v = self.value(k)
            map[k] = v
        return map

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
        self.image.delete_all()
        for k,v in dict.items():
            self.image.set(k, v)
    
    def __save(self, img_path):
        with open(img_path, 'wb') as f:
            f.write(self.image.get_file())


class ImageReader:
    def __init__(self, base_width=400):
        self.base_width = base_width

    def read(self, img_path):
        img = Image.open(img_path)
        width, height = img.size
        w_percent = (self.base_width / float(width))
        new_height = int((float(height) * float(w_percent)))
        return img.resize((self.base_width, new_height), Image.ANTIALIAS)