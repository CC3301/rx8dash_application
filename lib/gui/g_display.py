import tkinter


class GDisplay:
    def __init__(self, toplevel, config, sl):
        self.toplevel = toplevel
        self.config = config
        self.sl = sl

        self.bg = self.config.parser.get("application:gui", "background")
        self.fontcolor = self.config.parser.get("application:gui", "fontcolor")
        self.width, self.height = self.sl.getpos("d_display")['width_height']

        self.root = tkinter.Canvas(self.toplevel, highlightthickness=0, relief='ridge', bd=0, bg=self.bg,
                                   width=self.width, height=self.height)

        self.dots = [self.root.create_image(self.width/2, self.height/2, image=self.sl.assets['g_display_dot'])]
        self.lines = []

    def init(self):
        self.toplevel.create_window(self.sl.getpos("d_display")['anchor_nw'], anchor="nw", window=self.root)

    def update_dot_pos(self, pos_x, pos_y):
        pos_x = self.width/2+pos_x
        pos_y = self.height/2+pos_y

        p_pos_x, p_pos_y = self.root.coords(self.dots[-1])

        self.dots.append(self.root.create_image(pos_x, pos_y, image=self.sl.assets['g_display_dot']))
        if len(self.dots) > 10:
            self.root.delete(self.dots.pop(0))
            self.root.delete(self.lines.pop(0))

        self.lines.append(self.root.create_line(p_pos_x, p_pos_y, pos_x, pos_y, fill=self.fontcolor))
