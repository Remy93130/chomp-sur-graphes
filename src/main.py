#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""The main file for execute the project"""

# Global variables ------------------------------------------------------------

ARGS = None

# Imports ---------------------------------------------------------------------

# import sys
# import os
import argparse

import entity.parser as _parser
import entity.node as node
import entity.option as settings

# Functions -------------------------------------------------------------------

def manage_argv():
    global ARGS
    """Check argument given to the program"""
    argp = argparse.ArgumentParser()
    argp.add_argument("-nolog", help="Desactive les logs", action="store_true")
    argp.add_argument("-dev",   help="Logs dans la console", action="store_true")
    ARGS = argp.parse_args()

def setup():
    if ARGS.dev:
        settings.logs_output("console")
    elif ARGS.nolog:
        settings.logs_output(False)
    else:
        settings.logs_output("file")

def main():
    try:
        parser = _parser.Parser()
    except FileNotFoundError as exception:
        print("Erreur lors du parsage, lancer le programme depuis le dossier principal")
        raise exception

    nodes = parser.get_nodes()
    arrows = parser.get_arrows()
    node.initialize_edges(nodes, arrows)
    print(nodes)

if __name__ == '__main__':
    manage_argv()
    setup()
    main()
