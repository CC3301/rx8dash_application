import tkinter
import time


class GUI:
    def __init__(self, q):
        self.q = q
        self.toplevel = tkinter.Tk()
        self.toplevel.geometry("200x200")
        self.label = tkinter.Label(self.toplevel, text="test")
        self.label.pack()

    def update(self):
        time_start = time.time()
        current = self.q.get()
        time_end = time.time() - time_start
        print(f"{current} After: {time_end}")

        self.label.config(text=current)

        self.toplevel.update()
        self.toplevel.after(1, self.update)

    def start(self):
        self.update()
        self.toplevel.mainloop()
        print("TK Mainloop quit")