"""Module for the core game with turn"""

# Global variables ------------------------------------------------------------

TIME_FOR_PLAY = 20

# Imports ---------------------------------------------------------------------

import sys
from threading import Event
from .timer import Timer


# Classes ---------------------------------------------------------------------

class Game:
    """Class for the game count turn number and other"""

    def __init__(self):
        self.turn = 1
        self.end_of_thread = Event()

    def play(self):
        self.turn = (self.turn % 2) + 1

# Functions -------------------------------------------------------------------
