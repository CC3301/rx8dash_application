import tkinter


class GDisplay:
    def __init__(self, toplevel, config, sl):
        self.toplevel = toplevel
        self.config = config
        self.sl = sl

        self.bg = self.config.parser.get("application:gui", "background")
        self.fontcolor = self.config.parser.get("application:gui", "fontcolor")
        self.width, self.height = self.sl.getpos("d_display")['width_height']
        self.scale_factor = self.config.parser.get("application:gyr:factors", "scale_factor_accel")

        self.root = tkinter.Canvas(self.toplevel, highlightthickness=0, relief='ridge', bd=0, bg=self.bg,
                                   width=self.width, height=self.height)

        self.dots = [self.root.create_image(self.width/2, self.height/2, image=self.sl.assets['g_display_dot'])]
        self.readout = self.root.create_text(self.width/2, self.height - 15, text="test", fill=self.fontcolor)
        self.lines = []

    def init(self):
        self.toplevel.create_window(self.sl.getpos("d_display")['anchor_nw'], anchor="nw", window=self.root)

    def update(self, pos_x, pos_y):
        n_pos_x = (self.width/2) + (pos_x * int(self.scale_factor))
        n_pos_y = (self.height/2) + (pos_y * int(self.scale_factor))

        p_pos_x, p_pos_y = self.root.coords(self.dots[-1])

        self.dots.append(self.root.create_image(n_pos_x, n_pos_y, image=self.sl.assets['g_display_dot']))
        if len(self.dots) > 10:
            self.root.delete(self.dots.pop(0))
            self.root.delete(self.lines.pop(0))

        self.lines.append(self.root.create_line(p_pos_x, p_pos_y, n_pos_x, n_pos_y, fill=self.fontcolor))
        self.root.itemconfig(self.readout, text=f"X: {round(pos_x, 1)}, Y: {round(pos_y, 1)}")
