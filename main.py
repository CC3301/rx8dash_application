import sys

import logging
import queue
import time

from lib.signalhandler import SignalHandler

from lib.core import GUI
from lib.aggregator import SensorAggregator
from lib.configmanager import ConfigManager


class Main:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        configpath = sys.argv[1]  # first and only argument is the path to config
        self.config = ConfigManager(configpath)

        logging.basicConfig(level=self.config.loglevel(), format=self.config.loggingformat())

        self.logger.info("Starting rx8dash")
        self.q = queue.Queue()

        self.sensors = SensorAggregator(self.q)
        self.gui = GUI(self.q, self.config)

        self.logger.info("Initial setup complete, waiting for run() call")

    def run(self):
        self.sensors.start()
        while not self.sensors.ready():
            time.sleep(1)
        self.logger.info("sensor aggregator available, starting GUI")
        self.gui.start()

        # if we end up here, then the GUI has exited, and we should clean up
        self.stop()

    def stop(self):
        self.logger.info("Stopping rx8dash")
        self.gui.stop()
        self.sensors.stop()


if __name__ == '__main__':
    app = Main()
    SignalHandler(app)
    app.run()
