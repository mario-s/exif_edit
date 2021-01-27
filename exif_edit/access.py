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


class Writer:
    def __init__(self, image):
        self.image = image

    def save(self, dict, img_path):
        self.image.delete_all()
        for k,v in dict.items():
            self.image.set(k, v)
        with open(img_path, 'wb') as f:
            f.write(self.image.get_file())
