import queue

from lib.core import GUI
from lib.aggregator import SensorAggregator


class Main:
    def __init__(self):
        self.q = queue.Queue()
        self.gui = GUI(self.q)
        self.sensors = SensorAggregator(self.q)

    def run(self):
        self.sensors.start()
        self.gui.start()

        # if we end up here, then the GUI has exited and we should clean up
        self.sensors.stop()


if __name__ == '__main__':
    Main().run()
