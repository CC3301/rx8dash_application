import logging
import tkinter
import time

from lib.sensors.sensordataprocessor import SensorDataProcessor
from lib.gui.assetloader import AssetLoader


class GUI:
    def __init__(self, q, config):
        self.logger = logging.getLogger('lib.core.GUI')
        self.q = q
        self.config = config
        self.sdp = SensorDataProcessor(self.config)
        self.assetloader = AssetLoader()

        self.toplevel = tkinter.Tk()
        geometry = f"{self.config.windowwidth()}x{self.config.windowheight()}"
        self.toplevel.geometry(geometry)

        self.assetloader.load_all_assets()

        self.label = tkinter.Label(self.toplevel, text="test")
        self.label2 = tkinter.Label(self.toplevel, text="test2")
        self.label.pack()
        self.label2.pack()

    def update(self):
        # if there is no data available, wait for a short time and then retry the update
        if self.q.empty():
            self.toplevel.after(1, self.update)
            return

        # get and process available update
        self.sdp.process(self.q.get())

        self.label.config(text=self.sdp.rtcdate() + self.sdp.rtctime())
        self.label2.config(text=self.sdp.engine_oil_temp() + self.sdp.engine_water_temp())

        # reset the SDP and update the toplevel
        self.sdp.reset()
        self.toplevel.update()
        self.toplevel.after(1, self.update)

    def start(self):
        self.logger.info("Initiating MainLoop")
        start = time.time()
        self.update()
        self.toplevel.mainloop()
        delta = (time.time() - start) / 60
        self.logger.info(f"MainLoop exited after {delta} minutes")
