import logging
import tkinter
import time

from lib.sensors.sensordataprocessor import SensorDataProcessor
from lib.gui.assetloader import AssetLoader

from lib.gui.maingui import rootwindow
from lib.gui.frames import mainframe, topframe, bottomframe, oilpressureframe, oiltemperatureframe, \
    watertemperatureframe, rpmtachframe, timedateframe

from lib.gui.gauges import oil_pressure_gauge, oil_temperature_gauge, water_temperature_gauge, time_date_gauge


class GUI:
    def __init__(self, q, config):
        self.logger = logging.getLogger(__name__)
        self.q = q
        self.config = config
        self.al = AssetLoader()
        self.sdp = SensorDataProcessor(self.config)

        # get the toplevel window, we don't need more than that to load assets
        self.toplevel = rootwindow(self.config)
        self.toplevel.bind('<Control-t>', self.__stop_gui)
        self.al.load_all_assets()

        # frames
        self.mainframe = mainframe(self.toplevel, self.config, self.al)
        self.topframe = topframe(self.mainframe, self.config, self.al)
        self.bottomframe = bottomframe(self.mainframe, self.config, self.al)

        self.oilpressureframe = oilpressureframe(self.topframe, self.config, self.al)
        self.oiltemperatureframe = oiltemperatureframe(self.topframe, self.config, self.al)
        self.watertemperatureframe = watertemperatureframe(self.topframe, self.config, self.al)

        self.rpmtachframe = rpmtachframe(self.bottomframe, self.config, self.al)
        self.timedateframe = timedateframe(self.bottomframe, self.config, self.al)

        # gauges
        self.oil_pressure_gauge, self.oil_pressure_gauge_icon, self.oil_pressure_gauge_text = \
            oil_pressure_gauge(self.oilpressureframe, self.config, self.al)

        self.oil_temperature_gauge, self.oil_temperature_gauge_icon, self.oil_temperature_gauge_text = \
            oil_temperature_gauge(self.oiltemperatureframe, self.config, self.al)

        self.water_temperature_gauge, self.water_temperature_gauge_icon, self.water_temperature_gauge_text = \
            water_temperature_gauge(self.watertemperatureframe, self.config, self.al)

        self.time_date_gauge, self.time_date_gauge_time, self.time_date_gauge_date = \
            time_date_gauge(self.timedateframe, self.config, self.al)

    def update(self):
        # if there is no data available, don't do anything and try again
        if self.q.empty():
            self.toplevel.after(500, self.update)
            return

        # get and process available update
        self.sdp.process(self.q.get())

        self.oil_pressure_gauge.itemconfig(self.oil_pressure_gauge_text, text=self.sdp.engine_oil_pressure())
        self.oil_temperature_gauge.itemconfig(self.oil_temperature_gauge_text, text=self.sdp.engine_oil_temp())
        self.water_temperature_gauge.itemconfig(self.water_temperature_gauge_text, text=self.sdp.engine_water_temp())

        self.time_date_gauge.itemconfig(self.time_date_gauge_time, text=self.sdp.rtctime())
        self.time_date_gauge.itemconfig(self.time_date_gauge_date, text=self.sdp.rtcdate())

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

    def __stop_gui(self, event):
        self.stop()

    def stop(self):
        self.logger.info("Stopping MainLoop")
        try:
            self.toplevel.destroy()
        except tkinter.TclError as e:
            pass
