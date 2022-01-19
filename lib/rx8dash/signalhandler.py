import os, sys
import signal
import logging


# signal handler
class SignalHandler:
    def __init__(self, rx8dash):

        self.rx8dash = rx8dash

        self.logger = logging.getLogger('rx8dash.SignalHandler')
        self.logger.debug("Setting up signal handlers")

        signal.signal(signal.SIGINT, self._sigint_handler)
        self.logger.debug("SIGINT - Ok")

        self.logger.debug("Done setting up signal handlers")

    def _sigint_handler(self, signum, frame):
        self.logger.warn("SIGINT caught!")
        self.rx8dash.stop()
    
