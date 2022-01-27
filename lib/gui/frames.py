import tkinter


def mainframe(root, config, al):
    frame = tkinter.Frame(root, bg=config.mainbackgroundcolor())
    return frame.grid(column=0, row=0, padx=5, pady=5)


def topframe(root, config, al):
    frame = tkinter.Frame(root, bg=config.mainbackgroundcolor())
    return frame.grid(column=0, row=0, padx=0, pady=5)


def bottomframe(root, config, al):
    frame = tkinter.Frame(root, bg=config.mainbackgroundcolor())
    return frame.grid(column=0, row=1, padx=0, pady=50)


def oilpressureframe(root, config, al):
    frame = tkinter.Frame(root, bg=config.mainbackgroundcolor())
    return frame.grid(column=0, row=0, padx=0, pady=0)


def oiltemperatureframe(root, config, al):
    frame = tkinter.Frame(root, bg=config.mainbackgroundcolor())
    return frame.grid(column=1, row=0, padx=0, pady=0)


def watertemperatureframe(root, config, al):
    frame = tkinter.Frame(root, bg=config.mainbackgroundcolor())
    return frame.grid(column=2, row=0, padx=0, pady=0)


def rpmtachframe(root, config, al):
    frame = tkinter.Frame(root, bg=config.mainbackgroundcolor())
    return frame.grid(column=0, row=0, padx=0, pady=0)


def timedateframe(root, config, al):
    frame = tkinter.Frame(root, bg=config.mainbackgroundcolor())
    return frame.grid(column=1, row=0, padx=0, pady=0)