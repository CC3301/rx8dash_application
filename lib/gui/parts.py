import tkinter


def rootwindow(config):
    toplevel = tkinter.Tk()
    geometry = f"{config.parser.get('hardware:screen', 'width')}x{config.parser.get('hardware:screen', 'height')}"
    toplevel.geometry(geometry)
    toplevel.resizable(False, False)
    toplevel.config(bg=config.mainbackgroundcolor())
    toplevel.title('rx8dash')
    return toplevel


def base_canvas(root, config, sl):
    canvas = tkinter.Canvas(root, bg=config.mainbackgroundcolor(), highlightthickness=0, relief='ridge', bd=0,
                            width=config.parser.get("hardware:screen", "width"),
                            height=config.parser.get("hardware:screen", "height"))
    canvas.grid(column=0, row=0, padx=0, pady=0)
    background = canvas.create_image(1024/2, 600/2, image=sl.assets['background'])

    return canvas, background


def radial_gauge(root, config, sl, gauge_name):
    needle = root.create_image(sl.getpos(gauge_name)['needle_center_pos'], image=sl.assets['needle'])
    text = root.create_text(sl.getpos(gauge_name)['readout_top_left'], text="---", fill=config.mainfontcolor())

    return text, needle


def g_display(root, config, sl):
    x, y = sl.getpos('g_display_dot')['needle_center_pos']
    g_display_dot = root.create_image(x, y, image=sl.assets['g_display_dot'])

    return g_display_dot
