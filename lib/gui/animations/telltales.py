import time


class TellTales:
    def __init__(self, master, config, al):
        self.master = master
        self.config = config
        self.al = al
        self.__keep_running = True
        self.update = self.__do_nothing

    def load(self):
        self.al.rotate_template('needle', 0, 'needle_check')
        self.update = self.draw().__next__
        self.master.toplevel.after(100, self.update)

    def draw(self):
        angle = 0
        modifier = 1
        while self.__keep_running:
            self.al.rotate_template('needle_check', angle)
            self.master.oil_pressure_gauge.itemconfig(self.master.oil_pressure_gauge_needle,
                                                      image=self.al.templates['needle_check'])
            self.master.oil_temperature_gauge.itemconfig(self.master.oil_temperature_gauge_needle,
                                                         image=self.al.templates['needle_check'])
            self.master.water_temperature_gauge.itemconfig(self.master.water_temperature_gauge_needle,
                                                           image=self.al.templates['needle_check'])
            self.master.toplevel.after_idle(self.update)
            if angle >= 290:
                modifier = -1
            if modifier < 0 and angle < 5:
                self.stop()
            yield
            angle += modifier
            angle %= 360

    def stop(self):
        self.master.oil_pressure_gauge.itemconfig(self.master.oil_pressure_gauge_needle,
                                                  image=self.al.templates['needle'])
        self.master.oil_temperature_gauge.itemconfig(self.master.oil_temperature_gauge_needle,
                                                     image=self.al.templates['needle'])
        self.master.water_temperature_gauge.itemconfig(self.master.water_temperature_gauge_needle,
                                                       image=self.al.templates['needle'])
        self.__keep_running = False
        self.master.set_animation_lock(False)
        self.update = self.__do_nothing

    def __do_nothing(self, *args):
        pass
