import logging
import threading


class GenericCollector:
    def __init__(self, result_prefix):
        self.data = {}
        self.result_prefix = result_prefix
        self._readystate = False

        self.logger = logging.getLogger(f'lib.sensors.collector.GenericCollector({self.result_prefix})')
        self.t = threading.Thread(name="Collector", target=self._collect)

    def fetch(self):
        if not self._readystate:
            return {}
        return self.data

    def stop(self):
        self._readystate = False
        self.t.join()

    def start(self, i):
        self._readystate = True
        self.t.name = f"Collector#{i}"
        self.t.start()

    def _collect(self):
        pass
