import os, signal
import logging
import configparser


class StaticConfig:
    def __init__(self, configfile):
        self.logger = logging.getLogger("rx8dash.StaticConfig")
        self.logger.debug("Loading static configuration")
        self.cfile = configfile

        self.config = {}
        self.load()

    def load(self):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.cfile)
        except Exception as e:
            self.logger.fatal(f"Failed to load configuration: {e}")
            os.kill(os.getpid(), signal.SIGINT)
        self.logger.info(f"Loaded configuration: {self.cfile}")
