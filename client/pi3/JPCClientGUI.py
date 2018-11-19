import time
from tkinter import *


class JPCClientGUI:
    def __init__(self):
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.message_text = StringVar()
        self.message_text.set("Welcome")
        self.label = Label(self.root, textvariable=self.message_text,font=("Courier", 50), wraplength=500, justify=LEFT)
        self.label.pack()

    def start(self):
        self.root.update()
        self.root.update_idletasks()

    def flash_screen(self, color):
        self.label.configure(background=color)
        self.root.configure(background=color)
        self.root.update_idletasks()
        self.root.update()

    def set_message(self, message):
        self.message_text.set(message)
        for i in range(0,10):
            self.flash_screen("yellow")
            time.sleep(.1)
            self.flash_screen("red")
            time.sleep(.1)
        self.flash_screen("white")
        self.root.update_idletasks()
        self.root.update()
