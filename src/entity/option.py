"""Module for manage options like logs and
save or load game"""

# Global variables ------------------------------------------------------------

LOG_FILE = "log.txt"

# Imports ---------------------------------------------------------------------

import sys
import pickle


# Classes ---------------------------------------------------------------------

# Functions -------------------------------------------------------------------

def logs_output(output):
    """Redirect logs to the correct output
    depending of user choice in argument"""
    if output == "console":
        return
    elif output == "file":
        out = open(LOG_FILE, "w")
        sys.stdout = out
    else:
        sys.stdout = None
