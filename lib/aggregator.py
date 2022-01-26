import time
import logging
import threading

from lib.sensors.hardwaresensorcollector import HardwareSensorCollector
from lib.sensors.canbuscollector import CANBusCollector
from lib.sensors.rtctimecollector import RTCTimeCollector

from lib.sensors.sensordataprocessor import SensorDataProcessor


class SensorAggregator:
    def __init__(self, q):
        self.q = q

        self.logger = logging.getLogger('lib.aggregator.SensorAggregator')
        self.t = threading.Thread(name='SensorAggregator', target=self.collect_and_aggregate)

        self.__keep_running = False
        self.previous_result = {}

        self.collectors = [CANBusCollector('can'), HardwareSensorCollector('sensor'), RTCTimeCollector('rtc')]

    def start(self):
        self.__keep_running = True
        for i, collector in enumerate(self.collectors):
            collector.start(i)
        self.t.start()

    def stop(self):
        self.__keep_running = False
        for collector in self.collectors:
            collector.stop()
        self.t.join()

    def collect_and_aggregate(self):
        self.logger.info("Starting collector data aggregator")
        while self.__keep_running:
            result = {}
            for collector in self.collectors:
                result[str(collector.result_prefix)] = collector.fetch()

            if result != self.previous_result:
                self.previous_result = result
                self.q.put(result)

            # it will take some time until the collectors have collected new data (CAN speed, sensor value
            # interpretation)
            time.sleep(1)
        self.logger.warning("collector aggregator exited, this was either caused by an unhandled exception or intended "
                            "shutdown")
