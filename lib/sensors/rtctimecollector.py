import time

from lib.sensors.collector import GenericCollector


class RTCTimeCollector(GenericCollector):
    def __init__(self):
        super().__init__('rtc')
        self._setup()

    def _setup(self):
        pass

    def _collect(self):
        self.logger.debug(f"collector started")
        while self._readystate:
            self.data = {
                'time': time.time()
            }
            time.sleep(0.5)
        self.logger.debug("readystate changed to false")

