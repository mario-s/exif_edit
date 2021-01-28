from exif import Image


class Reader:
    def __init__(self, img_path):
        with open(img_path, 'rb') as f:
            self.image = Image(f)

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

class Writer:
    def __init__(self, image):
        self.image = image

    def save(self, collection, img_path):
        if type(collection) is dict:
            self.__set_values__(collection)
        elif type(collection) is list:
            d = self.__list_to_dict__(collection)
            self.__set_values__(d)
        else:
            raise ValueError("Expect either dict or list[list]!")

        self.__save__(img_path)

    def __list_to_dict__(self, list) -> dict:
        dict = {}
        for l in list:
            if len(l) < 2:
                raise ValueError("Expect at least two elements in the list")
            dict[l[0]] = l[1]
        return dict

    def __set_values__(self, dict):
        self.image.delete_all()
        for k,v in dict.items():
            self.image.set(k, v)
    
    def __save__(self, img_path):
        with open(img_path, 'wb') as f:
            f.write(self.image.get_file())
