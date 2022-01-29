import logging
import tkinter
import time

from lib.sensors.sensordataprocessor import SensorDataProcessor
from lib.gui.assetloader import AssetLoader

from lib.gui.maingui import rootwindow
from lib.gui.gauges import oil_pressure_gauge, oil_temperature_gauge, water_temperature_gauge, time_date_gauge, \
    map_canvas

from lib.gui.animations.startup import StartupAnimation
from lib.gui.animations.telltales import TellTales


class GUI:
    def __init__(self, q, rq, config, skip_startup):
        self.logger = logging.getLogger(__name__)
        self.q = q
        self.rq = rq
        self.config = config
        self.al = AssetLoader()
        self.sdp = SensorDataProcessor(self.config)

        self._skip_startup = skip_startup
        self._first_run = True
        self.animation_lock = False

        self.target_collectors = ['can', 'gps', 'sen']
        self.seen_collectors = []

        # get the toplevel window, we don't need more than that to load assets
        self.toplevel = rootwindow(self.config)
        self.toplevel.bind('<Control-t>', self.__stop_gui)
        self.al.load_all_assets()

        # frames
        self.mainframe = tkinter.Frame(self.toplevel, bg=config.mainbackgroundcolor())

        # startup animation
        self.startup_animation = StartupAnimation(self.toplevel, self.config, self.al)
        self.telltales_animation = TellTales(self, self.config, self.al)

        # gauges
        self.oil_pressure_gauge, self.oil_pressure_gauge_icon, self.oil_pressure_gauge_text, \
            self.oil_pressure_gauge_needle = oil_pressure_gauge(self.mainframe, self.config, self.al)

        self.oil_temperature_gauge, self.oil_temperature_gauge_icon, self.oil_temperature_gauge_text, \
            self.oil_temperature_gauge_needle = oil_temperature_gauge(self.mainframe, self.config, self.al)

        self.water_temperature_gauge, self.water_temperature_gauge_icon, self.water_temperature_gauge_text, \
            self.water_temperature_gauge_needle = water_temperature_gauge(self.mainframe, self.config, self.al)

        self.time_date_gauge, self.time_date_gauge_time, self.time_date_gauge_date = \
            time_date_gauge(self.mainframe, self.config, self.al)

        # self.map_canvas, self.map_canvas_map, self.map_canvas_location = map_canvas(self.mainframe, self.config, self.al)

    def first_update_cycle(self):
        if self._skip_startup is False:
            self.logger.info("running startup animation")
            self.startup_animation.load()
            self.check_ready()

        self.logger.info("Begin default GUI updatecycle")
        self._first_run = False
        self.mainframe.grid(column=0, row=0, padx=0, pady=0)
        self.telltales_animation.load()

    def check_ready(self):
        if self.rq.empty():
            if len(self.seen_collectors) == len(self.target_collectors):
                self.startup_animation.stop()
                self.logger.info("All collectors ready, stopping startup sequence")
            else:
                self.toplevel.after(500, self.check_ready)
        else:
            current = self.rq.get()
            self.logger.debug(f"'{current}' collector has become ready")
            self.seen_collectors.append(current)
            self.toplevel.after(500, self.check_ready)

    def set_animation_lock(self, boolean=True):
        self.animation_lock = boolean

    def update(self):
        # if an animation is in progress, we don't need to update the gui
        if self.animation_lock:
            self.logger.debug("animation in progress, waiting for animation end")
            self.toplevel.after(500, self.update)
            return

        # if we haven't updated for the first time, there is some more stuff to do
        if self._first_run:
            self.first_update_cycle()
            self.toplevel.after(500, self.update)
            return

        # if there is no data available, don't do anything and try again
        if self.q.empty():
            self.toplevel.after(1, self.update)
            return

        # get and process available update
        self.sdp.process(self.q.get())

        self.oil_pressure_gauge.itemconfig(self.oil_pressure_gauge_text,
                                           text=self.sdp.engine_oil_pressure)
        self.al.rotate_template('needle', self.sdp.engine_oil_pressure_needle_position, 'needle_oilp')
        self.oil_pressure_gauge.itemconfig(self.oil_pressure_gauge_needle,
                                           image=self.al.templates['needle_oilp'])
        self.oil_pressure_gauge.itemconfig(self.oil_pressure_gauge_icon,
                                           image=self.al.icons[f"oil_pressure_{self.sdp.engine_oil_pressure_status}"])

        self.oil_temperature_gauge.itemconfig(self.oil_temperature_gauge_text,
                                              text=self.sdp.engine_oil_temperature)
        self.al.rotate_template('needle', self.sdp.engine_oil_temperature_needle_position, 'needle_oilt')
        self.oil_temperature_gauge.itemconfig(self.oil_temperature_gauge_needle,
                                              image=self.al.templates['needle_oilt'])
        self.oil_temperature_gauge.itemconfig(self.oil_pressure_gauge_icon,
                                              image=self.al.icons[f"oil_temp_{self.sdp.engine_oil_temperature_status}"])

        self.water_temperature_gauge.itemconfig(self.water_temperature_gauge_text,
                                                text=self.sdp.engine_water_temperature)
        self.al.rotate_template('needle', self.sdp.engine_water_temperature_needle_position, 'needle_water')
        self.water_temperature_gauge.itemconfig(self.water_temperature_gauge_needle,
                                                image=self.al.templates['needle_water'])
        self.water_temperature_gauge.itemconfig(self.water_temperature_gauge_icon,
                                                image=self.al.icons[f"water_temp_{self.sdp.engine_water_temperature_status}"])

        self.time_date_gauge.itemconfig(self.time_date_gauge_time, text=self.sdp.gpstime)
        self.time_date_gauge.itemconfig(self.time_date_gauge_date, text=self.sdp.gpsdate)

        # update the toplevel
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
