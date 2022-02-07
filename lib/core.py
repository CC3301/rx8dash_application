import logging
import tkinter
import time

from lib.gui.skinloader import SkinLoader

from lib.gui.parts import rootwindow, base_canvas, radial_gauge, vehicle_speed
from lib.gui.info_display import InfoDisplay
from lib.gui.g_display import GDisplay


class GUI:
    def __init__(self, config, connection):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.connection = connection
        self.sl = SkinLoader(self.config)

        self.data = None

        self.target_collectors = ['can', 'gps', 'sen']
        self.seen_collectors = []

        # get the toplevel window, we don't need more than that to load assets
        self.toplevel = rootwindow(self.config)
        self.toplevel.bind('<Control-t>', self.__stop_gui)
        self.sl.load_skin()

        self.sl.resize_asset('g_display_dot', (3, 3), 'g_display_dot')

        self._update_end = 0
        self._update_start = 0

        # create base canvas
        self.base_canvas, self.background = base_canvas(self.toplevel, self.config, self.sl)

        # create gauges
        self.oil_pressure_gauge_text, self.oil_pressure_gauge_needle = radial_gauge(self.base_canvas, self.config,
                                                                                    self.sl, 'oil_pressure')
        self.oil_temperature_gauge_text, self.oil_temperature_gauge_needle = radial_gauge(self.base_canvas, self.config,
                                                                                          self.sl, 'oil_temp')
        self.water_temperature_gauge_text, self.water_temperature_gauge_needle = radial_gauge(self.base_canvas,
                                                                                              self.config, self.sl,
                                                                                              'water_temp')
        self.vehicle_speed_text = vehicle_speed(self.base_canvas, self.config, self.sl)

        self.g_display = GDisplay(self.base_canvas, self.config, self.sl)
        self.g_display.init()

        self.info_display = InfoDisplay(self.base_canvas, self.config, self.sl)
        self.info_display.init()

    def force_update(self, data):
        self.data = data
        self.update()

    def update(self):
        # if there is no data available, don't do anything and try again
        self.data = self.connection.fetch()
        if self.data is None:
            self.toplevel.after(100, self.update)
            return

        # update oil pressure gauge
        self.sl.rotate_asset('oil_pressure', 'needle', self.data['sen']['oil']['pressure']['needle_rotation'], 'needle_oilp')
        self.base_canvas.itemconfig(self.oil_pressure_gauge_text,
                                    text=self.data['sen']['oil']['pressure']['val'])
        self.base_canvas.itemconfig(self.oil_pressure_gauge_needle,
                                    image=self.sl.assets['needle_oilp'])

        # update oil temp gauge
        self.sl.rotate_asset('oil_temp', 'needle', self.data['sen']['oil']['temperature']['needle_rotation'], 'needle_oilt')
        self.base_canvas.itemconfig(self.oil_temperature_gauge_text,
                                    text=self.data['sen']['oil']['temperature']['val'])
        self.base_canvas.itemconfig(self.oil_temperature_gauge_needle,
                                    image=self.sl.assets['needle_oilt'])

        # update water temp gauge
        self.sl.rotate_asset('water_temp', 'needle', self.data['sen']['water']['temperature']['needle_rotation'], 'needle_water')
        self.base_canvas.itemconfig(self.water_temperature_gauge_text,
                                    text=self.data['sen']['water']['temperature']['val'])
        self.base_canvas.itemconfig(self.water_temperature_gauge_needle,
                                    image=self.sl.assets['needle_water'])

        # self.base_canvas.itemconfig(self.vehicle_speed_text, text=self.data['can']['vehicle']['velocity']['raw'])
        self.base_canvas.itemconfig(self.vehicle_speed_text, text="blyuat")

        # update info display
        # self.info_display.root.itemconfig(self.info_display.ups_counter, text=f"{int(self.connection.get_ups())} ups")
        # self.info_display.root.itemconfig(self.info_display.time, text=self.data['gps']['time']['time'])
        # self.info_display.root.itemconfig(self.info_display.date, text=self.data['gps']['time']['date'])

        # update g_display
        # self.g_display.update(self.data['gyr']['accel']['x'], self.data['gyr']['accel']['y'])

        # update the toplevel
        self.toplevel.update()
        self.toplevel.after(100, self.update)

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
