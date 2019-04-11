#!/usr/bin/python3
#-*- coding: utf-8 -*
"""[summary]

[description]
"""

GRAPH_FOLDER = "../ressources/graphes/"

import os
import pickle

def save_graph(new_name="", graph_name="Digraph.gv"):
    if not new_name:
        new_name = __get_graph_name()
    os.rename("./" + graph_name, GRAPH_FOLDER + new_name)
    os.remove(graph_name)

def __get_graph_name():
    """Function for generate a graph name if no one is given
    or the name already exist the name will be the number
    of the graph for example if they are already 3 graph
    created then the name will be 4

    Returns:
        str -- The new graph name
    """
    all_graphs = os.listdir(GRAPH_FOLDER)
    return str(len(all_graphs) + 1)

def serialize_graph(graph_path):
    """Parse the graph and serialize this one
    for avoid parse it every time we want use
    this one.    

    Arguments:
        graph_path {str} -- The relative path from the graph
    """
    pass


"""
pickle.dump(Object, open(filename, 'wb'))
object = pickle.load(open(filename, 'rb'))
"""