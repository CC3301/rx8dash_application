import logging
import random

import time

from lib.sensors.collector import GenericCollector


class HardwareSensorCollector(GenericCollector):
    def __init__(self):
        super().__init__('sen')
        self._setup()

    def _setup(self):
        pass

    def _collect(self):
        self.logger.info(f"collector started")
        while self._readystate:
            i = random.randint(0, 1000)
            self.data = {
                'oil': {
                    'temp': i,
                    'pressure': i
                },
                'water': {
                    'temp': i + 200
                }
            }
            time.sleep(0.5)
        self.logger.warning("readystate changed to false")

