#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""The main file for execute the project"""

# Global variables ------------------------------------------------------------

ARGS = None

# Imports ---------------------------------------------------------------------

from controller.controller import *
import argparse
import entity.option as settings
# import sys
# import os

# Functions -------------------------------------------------------------------

def manage_argv():
    """Manage arguments in program param
    for logs system
    """
    global ARGS
    argp = argparse.ArgumentParser()
    argp.add_argument("-nolog", help="Desactive les logs", action="store_true")
    argp.add_argument("-dev", help="Logs dans la console", action="store_true")
    ARGS = argp.parse_args()

def setup():
    """Select the good logs methods"""
    if ARGS.dev:
        settings.logs_output("console")
    elif ARGS.nolog:
        settings.logs_output(False)
    else:
        settings.logs_output("file")

def main():
    """The main boucle for the program"""
    controller();

if __name__ == '__main__':
    manage_argv()
    setup()
    main()