import tkinter as tk
from PIL import ImageTk
from PIL import Image

import random

# global variables
w = 'initial'

class Display(tk.Canvas):
    def __init__(self,  parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)


    def current_play(self, option):
        if option == 'initial':
            self.initial_display()
        elif option == 'n' or option == 's':
            self.ns_display()

    def initial_display(self):
        # display cat image
        self.im = Image.open("Rainier.jpg")
        self.photo_image = ImageTk.PhotoImage(self.im)
        self.demo = self.create_image(400, 400, image=self.photo_image, anchor='center')
        self.create_rectangle(50, 25, 150, 75, fill="blue")



class start_gui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self,parent, *args, **kwargs)
        # create canvas
        self.canvas = Display(parent, width=800, height=800, background="green")
        self.canvas.pack()
        self.canvas.current_play(w)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    start_gui(root)
    root.mainloop()
