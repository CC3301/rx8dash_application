import random
import time

from lib.sensors.collector import GenericCollector


class CANBusCollector(GenericCollector):
    def __init__(self):
        super().__init__('can')
        self._setup()

    def _setup(self):
        pass

    def _collect(self):
        self.logger.debug(f"collector started")
        while self._readystate:
            i = random.randint(0, 100)
            self.data = {
                'engine': {
                    'rpm': i,
                    'tps': i
                },
                'vehicle': {
                    'velocity': i
                }
            }
            time.sleep(self.delay)
        self.logger.debug("readystate changed to false")

