import time
import threading


class SensorAggregator:
    def __init__(self, q):
        self.q = q
        self.t = threading.Thread(name='SensorAggregator', target=self.collect_and_aggregate)
        self.__keep_running = False

    def start(self):
        self.__keep_running = True
        self.t.start()

    def stop(self):
        self.__keep_running = False
        self.t.join()

    def collect_and_aggregate(self):
        iterator = 0
        while self.__keep_running:
            self.q.put(f"test_string{iterator}")
            iterator += 1
            time.sleep(0.5)
