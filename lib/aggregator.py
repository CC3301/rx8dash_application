import time
import logging
import threading

from lib.sensors.hardwaresensorcollector import HardwareSensorCollector
from lib.sensors.canbuscollector import CANBusCollector
from lib.sensors.gpsdatacollector import GPSDataCollector


class SensorAggregator:
    def __init__(self, q, rq):
        self.q = q
        self.rq = rq

        self.logger = logging.getLogger(__name__)
        self.t = threading.Thread(name=__class__.__name__, target=self.collect_and_aggregate)

        self.__keep_running = False
        self.previous_result = {}

        self.collectors = [CANBusCollector(), HardwareSensorCollector(), GPSDataCollector()]

    def start(self):
        self.logger.debug("Starting collectors")
        self.__keep_running = True
        for i, collector in enumerate(self.collectors):
            collector.start(i)
            while not collector.ready():
                pass
            self.rq.put(f"{collector.result_prefix}")
        self.logger.debug("all collectors available, starting aggregator thread")
        self.t.start()

    def ready(self):
        return self.__keep_running

    def stop(self):
        self.__keep_running = False
        self.t.join()
        self.logger.debug("stopped SensorAggregator, waiting for collectors to exit")
        for collector in self.collectors:
            collector.stop()
            collector.t.join()
        self.logger.debug("SensorAggregator has exited")

    def collect_and_aggregate(self):
        self.logger.debug("SensorAggregator started")
        while self.__keep_running:
            result = {}
            for collector in self.collectors:
                result[str(collector.result_prefix)] = collector.fetch()

            if result != self.previous_result:
                self.previous_result = result
                self.q.put(result)

            # it will take some time until the collectors have collected new data (CAN speed, sensor value
            # interpretation)
            time.sleep(0.1)
        self.logger.debug("readystate changed to false")
