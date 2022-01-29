import sys

import logging
import queue
import threading

from lib.signalhandler import SignalHandler

from lib.core import GUI
from lib.aggregator import SensorAggregator
from lib.configmanager import ConfigManager


class Main:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if len(sys.argv) < 1:
            self.logger.critical("Cannot run without config!")
            sys.exit(1)

        skip_startup = False
        if len(sys.argv) > 2:
            if sys.argv[2] == 'no-startup':
                skip_startup = True

        configpath = sys.argv[1]
        self.config = ConfigManager(configpath)

        logging.basicConfig(level=self.config.loglevel(), format=self.config.loggingformat())

        self.logger.info("Starting rx8dash")
        self.q = queue.Queue()
        self.rq = queue.Queue()

        self.sensors = SensorAggregator(self.q, self.rq)
        self.gui = GUI(self.q, self.rq, self.config, skip_startup)

        self.sensor_starter = threading.Thread(target=self.sensors.start, name="SensorStarter")

        self.logger.debug("Initial setup complete, waiting for run() call")

    def run(self):
        self.sensor_starter.start()
        self.gui.start()

        # if we end up here, then the GUI has exited, and we should clean up
        self.stop()

    def stop(self):
        self.logger.info("Stopping rx8dash")
        self.sensor_starter.join()
        self.gui.stop()
        self.sensors.stop()


if __name__ == '__main__':
    app = Main()
    SignalHandler(app)
    app.run()
