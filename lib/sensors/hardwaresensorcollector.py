import logging
from lib.sensors.collector import GenericCollector


class HardwareSensorCollector(GenericCollector):
    def __init__(self, result_prefix):
        super().__init__(result_prefix)
        self._setup()

    def _setup(self):
        pass

    def _collect(self):
        self.logger.info(f"collector started")
        while self._readystate:
            for i in range(100):
                self.data = {
                    'oil': {
                        'temp': 300,
                        'pressure': i
                    },
                    'water': {
                        'temp': 300
                    }
                }
            pass
        self.logger.warning("collector stopped, this was either caused by an unhandled exception or intended shutdown")

