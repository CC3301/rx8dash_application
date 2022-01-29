import os
import sys
import glob
import logging

try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    try:
        from Pillow import Image, ImageTk
    except ModuleNotFoundError:
        sys.exit(3)

# disable DEBUG log for PIL
logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)


class AssetLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.templatepath = 'data/assets/templates'
        self.iconpath = 'data/assets/icons'

        self._templates_to_load = []
        self._icons_to_load = []

        for file in glob.glob(self.templatepath + '/*.png'):
            self._templates_to_load.append(file)

        for file in glob.glob(self.iconpath + '/*.png'):
            self._icons_to_load.append(file)

        self.templates = {}
        self.icons = {}

        self.raw_templates = {}
        self.raw_icons = {}

    def load_all_assets(self):
        self.load_templates()
        self.load_icons()

    def load_templates(self):
        self.logger.info(f"loading {len(self._templates_to_load)} templates")
        for file in self._templates_to_load:
            name = str(os.path.basename(file)).split('.')[0]
            self.logger.debug(f"loading template: {file} under name {name}")
            self.raw_templates[name] = Image.open(file)
            self.templates[name] = ImageTk.PhotoImage(self.raw_templates[name])

    def load_icons(self):
        self.logger.info(f"loading {len(self._icons_to_load)} icons")
        for file in self._icons_to_load:
            name = str(os.path.basename(file)).split('.')[0]
            self.logger.debug(f"loading icon: {file} under name {name}")
            self.raw_icons[name] = Image.open(file)
            self.icons[name] = ImageTk.PhotoImage(self.raw_icons[name])

    def rotate_template(self, name, angle, new_name=""):
        if angle > 290:
            angle = 290
        angle = 0 - angle
        if new_name == "":
            new_name = name
        self.raw_templates[new_name] = self.raw_templates[name]
        self.templates[new_name] = ImageTk.PhotoImage(self.raw_templates[name].rotate(angle))

    def crop_template(self, name, width, height, new_name=""):
        if new_name == "":
            new_name = name
        self.templates[new_name] = ImageTk.PhotoImage(self.raw_templates[name].resize(width, height))

    def rotate_icon(self, name, angle, new_name=""):
        if new_name == "":
            new_name = name
        self.icons[new_name] = ImageTk.PhotoImage(self.raw_icons[name].rotate(angle))

    def crop_icon(self, name, width, height, new_name=""):
        if new_name == "":
            new_name = name
        self.icons[new_name] = ImageTk.PhotoImage(self.raw_icons[name].resize(width, height))
