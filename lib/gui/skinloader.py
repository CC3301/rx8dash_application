import os
import sys
import glob
import logging
import json


from PIL import Image, ImageTk

# disable DEBUG log for PIL
logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)


class SkinLoader:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config

        self.__raw_assets = {}
        self.assets = {}

        self.skin_path = self.config.parser.get("application:gui", "skin_path")
        with open(self.skin_path + "/manifest.json", 'r') as f:
            self.manifest = json.load(f)
        f.close()

        with open(self.skin_path + "/" + self.manifest['gauge_positions']) as f:
            self.gauge_positions = json.load(f)
        f.close()

        self.logger.info(f"loading skin {self.skin_path}")

    def load_skin(self):
        # load assets
        for asset in self.manifest['assets']:
            self.__load_asset(asset, self.skin_path + "/" + self.manifest['assets'][asset])

    def __load_asset(self, asset, file):
        self.logger.debug(f"loading asset: '{asset}' ({file})")
        self.__raw_assets[asset] = Image.open(file)
        self.assets[asset] = ImageTk.PhotoImage(self.__raw_assets[asset])

    def getpos(self, gauge):
        return self.gauge_positions['gauges'][gauge]

    def rotate_asset(self, gauge, name, angle, new_name):
        if angle > int(self.config.parser.get("application:gauges", "max_angle")):
            angle = int(self.config.parser.get("application:gauges", "max_angle"))
        angle = 0 - angle
        self.assets[new_name] = ImageTk.PhotoImage(self.__raw_assets[name].rotate(angle), Image.ANTIALIAS)

    def resize_asset(self, name, scale, new_name):
        self.assets[new_name] = ImageTk.PhotoImage(self.__raw_assets[name].resize(scale), Image.ANTIALIAS)
