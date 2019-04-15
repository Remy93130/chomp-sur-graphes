"""Module for the graphic user interface
and interaction with the user"""

# Global variables ------------------------------------------------------------

ICON_PATH = "./ressources/images/ico.png"

# Imports ------------------------------------------------------------

from tkinter import Tk, Canvas, PhotoImage
from time import sleep


# Classes ---------------------------------------------------------------------

class GUI:
    """docstring for GUI"""

    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.tk.call("wm", "iconphoto", self.root._w, PhotoImage(file=ICON_PATH))
        self.root.title("Chomp sur Graphes")
        self.canvas = Canvas(self.root, width=725, height=725)
        self.canvas.bind("<Button-1>", self.on_rclick)
        self.canvas.pack()

    def on_rclick(self, event):
        """Callback when the user do a right click"""
        coord = event.x, event.y
        # Do something


def main():
    """Main for test the class"""
    global ICON_PATH
    ICON_PATH = "../../ressources/images/ico.png"
    root = Tk()
    GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
