import sys

import logging
import queue

from lib.core import GUI
from lib.aggregator import SensorAggregator
from lib.configmanager import ConfigManager


class Main:
    def __init__(self):
        self.logger = logging.getLogger('Main')

        configpath = sys.argv[1]  # first and only argument is the path to config
        self.config = ConfigManager(configpath)

        logging.basicConfig(level=logging.DEBUG, format=self.config.loggingformat())

        self.logger.info("Starting rx8dash")
        self.q = queue.Queue()

        self.gui = GUI(self.q, self.config)
        self.sensors = SensorAggregator(self.q)

    def run(self):
        self.sensors.start()
        self.gui.start()

        # if we end up here, then the GUI has exited, and we should clean up
        self.sensors.stop()


if __name__ == '__main__':
    Main().run()
