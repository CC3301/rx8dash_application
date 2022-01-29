import tkinter


def oil_pressure_gauge(root, config, al):
    canvas = tkinter.Canvas(root, bg=config.mainbackgroundcolor(), highlightthickness=0, relief='ridge', bd=0,
                            width=328, height=285)
    canvas.grid(column=0, row=0, padx=0, pady=0)
    canvas.create_image(174, 142, image=al.templates['small_gauge'])

    icon = canvas.create_image(174, 230, image=al.icons['oil_pressure_normal'])
    needle = canvas.create_image(174, 142, image=al.templates['needle'])
    text = canvas.create_text(174, 100, text="---", fill=config.mainfontcolor())

    return canvas, icon, text, needle


def oil_temperature_gauge(root, config, al):
    canvas = tkinter.Canvas(root, bg=config.mainbackgroundcolor(), highlightthickness=0, relief='ridge', bd=0,
                            width=328, height=285)
    canvas.grid(column=1, row=0, padx=0, pady=0)
    canvas.create_image(174, 142, image=al.templates['small_gauge'])

    icon = canvas.create_image(174, 230, image=al.icons['oil_temp_normal'])
    needle = canvas.create_image(174, 142, image=al.templates['needle'])
    text = canvas.create_text(174, 100, text="---", fill=config.mainfontcolor())

    return canvas, icon, text, needle


def water_temperature_gauge(root, config, al):
    canvas = tkinter.Canvas(root, bg=config.mainbackgroundcolor(), highlightthickness=0, relief='ridge', bd=0,
                            width=328, height=285)
    canvas.grid(column=2, row=0, padx=0, pady=0)
    canvas.create_image(174, 142, image=al.templates['small_gauge'])

    icon = canvas.create_image(174, 220, image=al.icons['water_temp_normal'])
    needle = canvas.create_image(174, 142, image=al.templates['needle'])
    text = canvas.create_text(174, 100, text="---", fill=config.mainfontcolor())

    return canvas, icon, text, needle


def time_date_gauge(root, config, al):
    canvas = tkinter.Canvas(root, bg=config.mainbackgroundcolor(), highlightthickness=0, relief='ridge', bd=0,
                            width=328, height=285)
    canvas.grid(column=1, row=1, padx=0, pady=0)
    time = canvas.create_text(174, 120, text="---", fill=config.mainfontcolor())
    date = canvas.create_text(174, 140, text="---", fill=config.mainfontcolor())

    return canvas, time, date

