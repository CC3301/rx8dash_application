import logging
import threading
import time


class SensorHandler:
    def __init__(self, config):
        self.logger = logging.getLogger('rx8dash.SensorHandler')
        self.logger.debug("Loading Sensors")

        self.config = config

        self.current_updateset = {}

        self.update = True

        self.updater_thread = threading.Thread(name='SensorUpdateThread', target=self._updater)
        self.updater_thread.start()

    def fetch(self):
        return self.current_updateset

    def stop(self):
        self.logger.warn("Received stop request, ending update loop")
        self.update = False

    def _updater(self):
        self.logger.debug("Initialized sensor update thread")

        val = 0
        while self.update:

            for i in range(15):
                val += 10
                self.current_updateset = {
                    "rtc": time.time(),
                    "amb": val,
                    "rpm": 800,
                    "tach": 0,
                    "oil": {
                        "pres": val,
                        "temp": val
                    },
                    "water": {
                        "temp": val
                    }
                }
                time.sleep(0.3)
            val = 0

        self.logger.debug("Update loop exited, assuming stop condition")
