import logging
import tkinter
import os

class GUI:
    def __init__(self, config, sensors):
        self.logger = logging.getLogger('rx8dash.GUI')
        self.logger.debug("Loading GUI")

        self.config = config
        self.sensors = sensors

        self.width  = int(self.config.config['hardware:screen']['width'])
        self.height = int(self.config.config['hardware:screen']['height'])
        self.xpos   = int(self.width / 2)
        self.ypos   = int(self.height / 2)

        # fetch initial sensor data
        self.values = self.sensors.fetch()
        
        self._setup()


    def _setup(self):
        self.logger.debug("setting up core gui")
        self._toplevel = tkinter.Tk()
        self._toplevel.geometry(f"{self.width}x{self.height}+{self.xpos}+{self.ypos}")

        # load frames and canvasses
        self._frames()
        self.logger.debug("framing complete")
        self._canvasses()
        self.logger.debug("canvasses set up")
        
        self._aux_frame.pack()

        #self._oil_pres_frame.pack()
        #self._oil_pres_canvas.pack()
        #self._oil_pres_readout.pack()

        self._oil_temp_frame.pack()
        self._oil_temp_canvas.pack()

        coord = 10, 50, 240, 210
        image = tkinter.PhotoImage(os.getcwd() + "/gimp/gauge_template.bmp")
        self._oil_temp_canvas.create_image(10,10, image = image, anchor="nw")
        # arc = self._oil_pres_canvas.create_arc(coord,   start = 0, extent = 150, fill = "blue")
        # arc = self._oil_temp_canvas.create_arc(coord, start = 0, extent = 150, fill = "green")
        # arc = self._water_temp_canvas.create_arc(coord, start = 0, extent = 150, fill = "red")


    def run_gui(self):
        self.update_gui()

        self.logger.debug("calling toplevel.mainloop()")
        self._toplevel.mainloop()

    def update_gui(self):
        self.values = self.sensors.fetch()
        self._canvasses()
        self._toplevel.update()
        self._toplevel.after(100, self.update_gui)
        

    #==========================================================================
    # frames
    #==========================================================================
    def _frames(self):
        self.__rpm_frame()
        self.__tach_frame()
        self.__aux_frame()
        self.__oil_pres_frame()
        self.__oil_temp_frame()
        self.__water_temp_frame()

    def __rpm_frame(self):
        self._rpm_frame = tkinter.Frame(self._toplevel)
    
    def __tach_frame(self):
        self._tach_frame = tkinter.Frame(self._toplevel)

    def __aux_frame(self):
        self._aux_frame = tkinter.Frame(self._toplevel)

    def __oil_pres_frame(self):
        self._oil_pres_frame = tkinter.Frame(self._aux_frame)
    
    def __oil_temp_frame(self):
        self._oil_temp_frame = tkinter.Frame(self._aux_frame)
    
    def __water_temp_frame(self):
        self._water_temp_frame = tkinter.Frame(self._aux_frame)

    #==========================================================================
    # canvasses
    #==========================================================================
    def _canvasses(self):     
        self.__rpm_canvas()
        self.__tach_canvas()
        self.__oil_pres_canvas()
        self.__oil_temp_canvas()
        self.__water_temp_canvas()
        
    def __rpm_canvas(self):
        self._rpm_canvas = tkinter.Canvas(self._rpm_frame)

    def __tach_canvas(self):
        self._tach_canvas = tkinter.Canvas(self._tach_frame)

    def __oil_pres_canvas(self):

        if hasattr(self, '_oil_pres_readout'):
            self._oil_pres_readout.config(text=self.values['oil']['pres'])
        else:
            self._oil_pres_readout = tkinter.Label(self._oil_pres_frame, text=self.values['oil']['pres'])

        self._oil_pres_canvas = tkinter.Canvas(self._oil_pres_frame)
        
        self._oil_pres_canvas.pack()
        self._oil_pres_readout.pack()

    def __oil_temp_canvas(self):
        self._oil_temp_canvas = tkinter.Canvas(self._oil_temp_frame, width=328, height=285)

    def __water_temp_canvas(self):
        self._water_temp_canvas = tkinter.Canvas(self._water_temp_frame)