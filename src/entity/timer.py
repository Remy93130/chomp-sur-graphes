"""Module for manage the time in the game"""

# Imports ---------------------------------------------------------------------

import time as t


# Classes ---------------------------------------------------------------------

class Timer:
    """Class for create a countdown during the game"""

    def __init__(self, gui, location, max_time):
        self.gui = gui
        self.begin = 0
        self.previous = 0
        self.now = 0
        self.location = location
        self.max_time = max_time
        self.IsStop = False
        self.isPause = True
        self.showing = True

    def hide(self):

        self.showing = False

    def show(self):
        self.showing = True

    def start(self):
        """Method for launch or relaunch the timer"""
        if self.isPause:
            self.begin = t.time()
            self.isPause = False

    def stop(self):
        self.IsStop = True

    def pause(self):
        """Method for stop the timer"""
        if not self.isPause:
            self.begin = 0
            self.previous = self.now
            self.isPause = True

    def run(self):
        """Method for run the timer"""
        if self.IsStop:
            return
        if self.begin == 0:
            self.now = self.previous
        else:
            self.now = self.previous + t.time() - self.begin
        if self.max_time - self.now < 0:
            return "done"
        minutes, sec = divmod(self.max_time - self.now, 60)
        hou, minutes = divmod(minutes, 60)
        if self.showing:
            time = "%d:%02d:%02d" % (hou, minutes, sec)
        else:
            time = ""
        self.gui.canvas.itemconfigure(self.location, text=time)
        self.gui.screen.after(1000, self.run)

# Functions -------------------------------------------------------------------
