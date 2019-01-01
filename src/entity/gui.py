"""Module for the graphic user interface
and interaction with the user"""

# Imports ------------------------------------------------------------

from tkinter import Tk

# Classes ---------------------------------------------------------------------

class GUI:
    """docstring for GUI"""
    def __init__(self, root):
        self.root = root
        root.title("Chomp sur Graphes")

def main():
    """Main for test the class"""
    root = Tk()
    GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
