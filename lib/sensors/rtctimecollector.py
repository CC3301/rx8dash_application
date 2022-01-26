import time

from lib.sensors.collector import GenericCollector


class RTCTimeCollector(GenericCollector):
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
                    'time': time.time()
                }
            pass
        self.logger.warning("collector stopped, this was either caused by an unhandled exception or intended shutdown")

