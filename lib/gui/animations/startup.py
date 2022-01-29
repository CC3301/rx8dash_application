import tkinter


class StartupAnimation:
    def __init__(self, master, config, al):
        self.master = master
        self.config = config
        self.al = al
        self.canvas = tkinter.Canvas(master, width=1024, height=600, bg=self.config.mainbackgroundcolor(),
                                     relief='ridge', highlightthickness=0, bd=0
                                     )
        self.__keep_running = True
        self.update = self.__do_nothing

    def load(self):
        self.al.rotate_template('rotor', 0, 'rotor_start')
        self.canvas.create_image(1024 / 2, 600 / 2, image=self.al.templates['start_screen'])
        self.canvas.grid(column=0, row=0)
        self.update = self.draw().__next__
        self.master.after(100, self.update)

    def draw(self):
        angle = 0
        while self.__keep_running:
            self.al.rotate_template('rotor_start', angle)
            canvas_obj = self.canvas.create_image(768, 300, image=self.al.templates['rotor_start'])
            self.master.after_idle(self.update)
            yield
            self.canvas.delete(canvas_obj)
            angle += 1.5
            angle %= 360

        self.canvas.destroy()

    def stop(self):
        self.__keep_running = False
        self.update = self.__do_nothing

    def __do_nothing(self, *args):
        pass
