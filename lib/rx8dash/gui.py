import logging
import tkinter
import os
from PIL import Image, ImageTk
from datetime import datetime


class GUI:
    def __init__(self, config, sensors):
        self.logger = logging.getLogger('rx8dash.GUI')
        self.logger.debug("Loading GUI")

        self.config = config
        self.sensors = sensors

        self.width = int(self.config.config['hardware:screen']['width'])
        self.height = int(self.config.config['hardware:screen']['height'])
        self.xpos = int(self.width / 2)
        self.ypos = int(self.height / 2)

        # fetch initial sensor data
        self.values = self.sensors.fetch()

        self._setup()

    def _setup(self):
        # grab some frequently used values from the config
        bg = self.config.config['application:gui']['background']
        fc = self.config.config['application:gui']['fontcolor']

        # toplevel window
        self.logger.debug("Setting up core gui")
        self._toplevel = tkinter.Tk()
        self._toplevel.geometry(f"{self.width}x{self.height}+{self.xpos}+{self.ypos}")
        self._toplevel.config(bg=bg)
        self._toplevel.title("rx8dash")
        self._toplevel.resizable(False, False)

        # load assets
        self._load_assets()

        # main frame containing the entire gui
        self._main_frame = tkinter.Frame(self._toplevel, bg=bg)
        self._main_frame.pack(padx=5, pady=5, expand=1, fill="both")

        # secondary and aux frames
        self._aux_frame = tkinter.Frame(self._main_frame, bg=bg)
        self._aux_frame.grid(column=0, row=0, padx=0, pady=5)

        self._secondary_frame = tkinter.Frame(self._main_frame, bg=bg)
        self._secondary_frame.grid(column=0, row=1, padx=0, pady=50)

        # aux gauges
        self._oil_pres_frame = tkinter.Frame(self._aux_frame, bg=bg, borderwidth=0)
        self._oil_pres_frame.grid(column=0, row=0, padx=5, pady=0)

        self._oil_temp_frame = tkinter.Frame(self._aux_frame, bg=bg, width=328, height=285)
        self._oil_temp_frame.grid(column=1, row=0, padx=0, pady=0)

        self._water_temp_frame = tkinter.Frame(self._aux_frame, bg=bg, width=328, height=285)
        self._water_temp_frame.grid(column=2, row=0, padx=0, pady=0)

        # secondary gauges
        self._rpm_frame = tkinter.Frame(self._secondary_frame, bg="yellow", width=328, height=195)
        self._rpm_frame.grid(column=0, row=0, padx=0, pady=0)

        self._time_amb_temp_frame = tkinter.Frame(self._secondary_frame, bg=bg, width=328, height=195)
        self._time_amb_temp_frame.grid(column=1, row=0, padx=5, pady=0)

        self._tach_frame = tkinter.Frame(self._secondary_frame, bg="lightblue", width=328, height=195)
        self._tach_frame.grid(column=2, row=0, padx=0, pady=0)

        # aux gauges
        self._oil_pres_canvas = tkinter.Canvas(self._oil_pres_frame, width=328, height=285, bd=0, bg=bg,
                                               highlightthickness=0, relief='ridge')
        self._oil_pres_canvas.pack(padx=0, pady=0, expand=1, fill='both')
        self._oil_pres_canvas.create_image(174, 142, image=self.__small_gauge_template)
        self._oil_pres_icon = self._oil_pres_canvas.create_image(174, 220, image=self.__oil_pres_icon)
        self._oil_pres_readout = self._oil_pres_canvas.create_text(174, 100, text="--- bar", fill=fc)

        self._oil_temp_canvas = tkinter.Canvas(self._oil_temp_frame, width=328, height=285, bd=0, bg=bg,
                                               highlightthickness=0, relief='ridge')
        self._oil_temp_canvas.pack(padx=0, pady=0, expand=1, fill='both')
        self._oil_temp_canvas.create_image(174, 142, image=self.__small_gauge_template)
        self._oil_temp_icon = self._oil_temp_canvas.create_image(174, 220, image=self.__oil_temp_icon)
        self._oil_temp_readout = self._oil_temp_canvas.create_text(174, 100, text="--- °C", fill=fc)

        self._water_temp_canvas = tkinter.Canvas(self._water_temp_frame, width=328, height=285, bd=0, bg=bg,
                                                 highlightthickness=0, relief='ridge')
        self._water_temp_canvas.pack(padx=0, pady=0, expand=1, fill='both')
        self._water_temp_canvas.create_image(174, 142, image=self.__small_gauge_template)
        self._water_temp_icon = self._water_temp_canvas.create_image(174, 220, image=self.__water_temp_icon)
        self._water_temp_readout = self._water_temp_canvas.create_text(174, 100, text="--- °C", fill=fc)

        # secondary gauges
        self._rtc_date_label = tkinter.Label(self._time_amb_temp_frame, bg=bg, fg=fc)
        self._rtc_date_label.grid(column=0, row=0)

        self._rtc_time_label = tkinter.Label(self._time_amb_temp_frame, bg=bg, fg=fc)
        self._rtc_time_label.grid(column=0, row=1)

        self._amb_temp_label = tkinter.Label(self._time_amb_temp_frame, bg=bg, fg=fc)
        self._amb_temp_label.grid(column=0, row=2)

    def run_gui(self):
        self.update_gui()

        self.logger.debug("calling toplevel.mainloop()")
        self._toplevel.mainloop()

    def update_gui(self):
        self.values = self.sensors.fetch()

        # update date, time and amb temp
        self._rtc_date_label.config(text=str(datetime.fromtimestamp(self.values['rtc']).strftime('%d.%m.%Y')))
        self._rtc_time_label.config(text=str(datetime.fromtimestamp(self.values['rtc']).strftime('%H:%M:%S')))
        self._amb_temp_label.config(text=f"{('+' if self.values['amb'] > 0 else '') + str(self.values['amb'])} °C")

        # update water temp gauge
        if self.values['water']['temp'] < 80:
            self.__water_temp_icon = self.__water_temp_icon_blue
        elif 80 <= self.values['water']['temp'] < 100:
            self.__water_temp_icon = self.__water_temp_icon_normal
        else:
            self.__water_temp_icon = self.__water_temp_icon_red

        self._water_temp_canvas.itemconfig(self._water_temp_icon, image=self.__water_temp_icon)
        self._water_temp_canvas.itemconfig(self._water_temp_readout,
                                           text=f"{('+' if self.values['water']['temp'] > 0 else '') + str(self.values['water']['temp'])} °C")

        # update oil temp gauge
        if self.values['oil']['temp'] < 80:
            self.__oil_temp_icon = self.__oil_temp_icon_blue
        elif 80 <= self.values['oil']['temp'] < 100:
            self.__oil_temp_icon = self.__oil_temp_icon_normal
        else:
            self.__oil_temp_icon = self.__oil_temp_icon_red

        self._oil_temp_canvas.itemconfig(self._oil_temp_icon, image=self.__oil_temp_icon)
        self._oil_temp_canvas.itemconfig(self._oil_temp_readout,
                                         text=f"{('+' if self.values['oil']['temp'] > 0 else '') + str(self.values['oil']['temp'])} °C")

        # update oil pressure gauge
        if self.values['oil']['pres'] < 80:
            self.__oil_pres_icon = self.__oil_pres_icon_blue
        elif 80 <= self.values['oil']['pres'] < 100:
            self.__oil_pres_icon = self.__oil_pres_icon_normal
        else:
            self.__oil_pres_icon = self.__oil_temp_icon_red

        self._oil_pres_canvas.itemconfig(self._oil_pres_icon, image=self.__oil_pres_icon)
        self._oil_pres_canvas.itemconfig(self._oil_pres_readout,
                                         text=f"{self.values['oil']['pres']} bar")

        self._toplevel.update()
        self._toplevel.after(1, self.update_gui)

    def _load_assets(self):
        self.logger.info("Loading assets")
        self.__small_gauge_template = ImageTk.PhotoImage(
            Image.open(f"data/assets/templates/{self.config.config['application:gui']['small_gauge_template']}")
                .resize((328, 285), Image.ANTIALIAS)
        )

        # water temp icons
        self.__water_temp_icon_blue = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/water_temp_blue.png").resize((65, 54), Image.ANTIALIAS)
        )
        self.__water_temp_icon_red = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/water_temp_red.png").resize((65, 54), Image.ANTIALIAS)
        )
        self.__water_temp_icon_normal = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/water_temp_normal.png").resize((65, 54), Image.ANTIALIAS)
        )

        # oil temp icons
        self.__oil_temp_icon_blue = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/oil_temp_blue.png").resize((80, 80), Image.ANTIALIAS)
        )
        self.__oil_temp_icon_red = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/oil_temp_red.png").resize((80, 80), Image.ANTIALIAS)
        )
        self.__oil_temp_icon_normal = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/oil_temp_normal.png").resize((80, 80), Image.ANTIALIAS)
        )

        # oil pressure icons
        self.__oil_pres_icon_blue = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/oil_pressure_blue.png").resize((80, 80), Image.ANTIALIAS)
        )
        self.__oil_pres_icon_red = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/oil_pressure_red.png").resize((80, 80), Image.ANTIALIAS)
        )
        self.__oil_pres_icon_normal = ImageTk.PhotoImage(
            Image.open("data/assets/aux_gauges/icons/oil_pressure_normal.png").resize((80, 80), Image.ANTIALIAS)
        )

        # set defaults
        self.__water_temp_icon = self.__water_temp_icon_normal
        self.__oil_temp_icon = self.__oil_temp_icon_normal
        self.__oil_pres_icon = self.__oil_pres_icon_normal

        self.logger.info("Finished loading assets")
