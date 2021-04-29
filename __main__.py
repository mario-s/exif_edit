import click

from exif_edit.gui import App


@click.command()
@click.option("--img",
    help="The path to the image which should be loaded on start.")
def start(img):
    app = App()
    if not img is None:
        app.load_image(img)
    app.start()

if __name__ == "__main__":
   start()
