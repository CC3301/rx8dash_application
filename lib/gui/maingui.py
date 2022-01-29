import tkinter


def rootwindow(config):
    toplevel = tkinter.Tk()
    geometry = f"{config.windowwidth()}x{config.windowheight()}"
    toplevel.geometry(geometry)
    toplevel.resizable(False, False)
    toplevel.config(bg=config.mainbackgroundcolor(), padx=20)
    toplevel.title('rx8dash')
    return toplevel
