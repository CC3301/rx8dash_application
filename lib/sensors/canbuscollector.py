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
        self.logger.info(f"collector started")
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
            time.sleep(0.5)
        self.logger.warning("readystate changed to false")

