#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""The main file for execute the project"""

# Imports ---------------------------------------------------------------------

# import sys
# import os

import entity.parser as _parser
from entity.node import delete_node

# Functions -------------------------------------------------------------------

def create_edges(nodes, arrows):
    for arrow in arrows:
        nodes[arrow.id_arrow[0]].set_edges(arrow.id_arrow[1])

def main():
    try:
        parser = _parser.Parser('./ressources/1.gv.svg')
    except FileNotFoundError as exception:
        print("Erreur lors du parsage, lancer le programme depuis le dossier principal")
        raise exception

    nodes = parser.get_nodes()
    arrows = parser.get_arrows()
    create_edges(nodes, arrows)

if __name__ == '__main__':
    main()
