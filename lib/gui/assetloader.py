import glob
import logging
import tkinter
from PIL import Image, ImageTk


class Template:
    def __init__(self, image, path, name):
        self.image = image
        self.path = path
        self.name = name


class Icon:
    def __init__(self, image, path, name):
        self.image = image
        self.path = path
        self.name = name


class AssetLoader:
    def __init__(self):
        self.logger = logging.getLogger('lib.gui.assetloader.AssetLoader')

        self.templatepath = 'data/assets/templates'
        self.iconpath = 'data/assets/icons'

        self._templates_to_load = []
        self._icons_to_load = []

        for file in glob.glob(self.templatepath + '/*.png'):
            self._templates_to_load.append(file)

        for file in glob.glob(self.iconpath + '/*.png'):
            self._icons_to_load.append(file)

        self.templates = []
        self.icons = []

    def load_all_assets(self):
        self.load_templates()
        self.load_icons()

    def load_templates(self):
        self.logger.info(f"loading {len(self._templates_to_load)} templates")
        for file in self._templates_to_load:
            self.templates.append(Template(ImageTk.PhotoImage(Image.open(f"{file}")), file, file))

    def load_icons(self):
        self.logger.info(f"loading {len(self._icons_to_load)} icons")
        for file in self._icons_to_load:
            self.icons.append(Icon(ImageTk.PhotoImage(Image.open(f"{file}")), file, file))
