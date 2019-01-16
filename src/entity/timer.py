"""Module for manage the time in the game"""

# Imports ---------------------------------------------------------------------

import time as t

# Classes ---------------------------------------------------------------------

class Timer:
	"""Class for create a coutdown during the game"""
	def __init__(self, gui, location, max_time):
		self.gui = gui
		self.begin = t.time()
		self.location = location
		self.max_time = max_time*60

	def run(self):
		"""Method for run the timer"""
		now = t.time() - self.begin
		if(self.max_time-now < 0):
			return "done"
		min, sec = divmod(self.max_time-now, 60)
		hou,min = divmod(min, 60)
		time = "%d:%02d:%02d" % (hou, min, sec)
		self.gui.canvas.itemconfigure(self.location, text=time)
		self.gui.screen.after(1000, self.run)

# Functions -------------------------------------------------------------------

