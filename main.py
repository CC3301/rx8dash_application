import sys
import logging

from lib.signalhandler import SignalHandler

from lib.core import GUI
from lib.connection import Connection
from lib.configmanager import ConfigManager


class Main:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if len(sys.argv) < 1:
            self.logger.critical("Cannot run without config!")
            sys.exit(1)

        configpath = sys.argv[1]
        self.config = ConfigManager(configpath)

        logging.basicConfig(level=self.config.loglevel(), format=self.config.loggingformat())

        self.logger.info("Starting rx8dash")

        self.connection = Connection(self.config.parser.get("application:data_provider", "remote_addr"),
                                     self.config.parser.get("application:data_provider", "remote_port"))
        self.gui = GUI(self.config, self.connection)

        self.logger.debug("Initial setup complete, waiting for run() call")

    def run(self):
        self.connection.start()
        self.gui.start()

        # if we end up here, then the GUI has exited, and we should clean up
        self.stop()

    def stop(self):
        self.logger.info("Stopping rx8dash")
        self.gui.stop()
        self.connection.stop()


def main():
    app = Main()
    SignalHandler(app)
    app.run()


if __name__ == '__main__':
    main()
