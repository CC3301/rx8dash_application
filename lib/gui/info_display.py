import tkinter


class InfoDisplay:
    def __init__(self, toplevel, config, sl):
        self.toplevel = toplevel
        self.config = config
        self.sl = sl

        self.bg = self.config.parser.get("application:gui", "background")
        self.fontcolor = self.config.parser.get("application:gui", "fontcolor")

        self.root = tkinter.Canvas(self.toplevel, highlightthickness=0, relief='ridge', bd=0, bg=self.bg,
                                   width=self.sl.getpos("info_display")['width_height'][0],
                                   height=self.sl.getpos("info_display")['width_height'][1])

        self.time = self.root.create_text(50, 10, text="time", fill=self.fontcolor)
        self.date = self.root.create_text(50, 30, text="date", fill=self.fontcolor)
        self.ups_counter = self.root.create_text(50, 50, text="--- fps", fill=self.fontcolor)

    def init(self):
        self.toplevel.create_window(self.sl.getpos("info_display")['anchor_nw'], anchor="nw", window=self.root)

    def set_time_date(self, time, date):
        self.root.itemconfig(self.time, text=time)
        self.root.itemconfig(self.date, text=date)
