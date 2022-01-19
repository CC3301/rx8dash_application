import sys
import logging
import threading
import queue

from lib.rx8dash.signalhandler import SignalHandler
from lib.config import StaticConfig
from lib.rx8dash.sensors import SensorHandler
from lib.rx8dash.gui import GUI


# main entrypoint
class rx8dash:
    def __init__(self, logger, configfile):
        self.logger = logger
        self.logger.debug("Setting up core components")

    def run(self):
        # load config
        self.config = StaticConfig(configfile)

        # create and run SensorHandler
        self.sensors = SensorHandler(self.config)
        
        # create and run GUI
        self.gui = GUI(self.config, self.sensors)
        self.gui.run_gui()
    
    def stop(self):
        self.logger.info("Received stop request, ending threads")

        self.sensors.stop()
        self.sensors.updater_thread.join()

        self.logger.info("All remaining threads have exited, shutting down")

        # exit with clean 0 when using stop()
        sys.exit(0)

        
# setup logger and signal handlers
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('rx8dash.main')
    logger.info("Starting rx8dash")

    # set up signal handlers
    

    # check config file
    logger.debug("checking for config file")
    if not len(sys.argv) > 1:
        logger.fatal("Config file not found - aborting")
        sys.exit(0)
    else:
        configfile = sys.argv[1]

    # start rx8dash
    logger.debug("Pre-requisits checked, starting actual dash")
    dash = rx8dash(logger, configfile)
    SignalHandler(dash)
    dash.run()
