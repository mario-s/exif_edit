import os
import sys

from exif_edit.app import App

if __name__ == "__main__":
    def img_path():
        img_path = os.path.realpath('./exif_edit/test/resources/lookup.jpg')
        args_len = len(sys.argv) - 1
        if args_len > 0:
            img_path = os.path.realpath(sys.argv[1])
        return img_path

    app = App()
    app.load_image(img_path())
    app.mainloop()