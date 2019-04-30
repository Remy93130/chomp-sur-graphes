#!/usr/bin/python3
#-*- coding: utf-8 -*
"""[summary]
[description]
"""

GRAPH_FOLDER = "../ressources/graphes/"

import os
import pickle

import parser
from graphviz import Digraph, render


class manuelGeneration:
	def __init__(self,string):
		self.string = string
		self.generated = Digraph(format="svg", engine="sfdp")
	
	def create(self):
		liste = []
		instruction = 1
		number = ""
		for char in self.string:
			if instruction == 1:
				if char.isdigit():
					number += char
				elif char.isspace():
					continue
				elif char == 'p':
					if number != "":
						self.generated.node(number,color="lightblue", style="filled")
						number = ""
				elif char == ';':
					if number != "":
						self.generated.node(number)
						number = ""  
					instruction+=1
				elif char.isdigit() == False:
					if number != "":
						self.generated.node(number)
						number = ""
					continue
			elif instruction != 1:
				if char.isdigit():
					number += char
				elif char.isspace():
					continue
				elif char == ';':
					if number != "":
						liste.append(int(number))
						number = ""  
					self.init_edge(liste)
					instruction+=1
					liste = []
				elif char.isdigit() == False:
					if number != "":
						liste.append(int(number))
					number = ""
		self.generated.render()
		render("sfdp", "svg", "Digraph.gv")
	
	def init_edge(self,liste):
		pred = liste.pop(0)
		for succ in liste:
			self.generated.edge(str(pred),str(succ))
			
	def display_graph(self):
		self.generated.view()

def save_graph(new_name="", graph_name="Digraph.gv.svg"):
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
    return str(len(all_graphs) + 1)+".svg"

def serialize_graph(graph, path):
    pickle.dump(graph, open(path, "wb"))

def load_graph(path):
    return pickle.load(open(path, "rb"))

"""
pickle.dump(Object, open(filename, 'wb'))
object = pickle.load(open(filename, 'rb'))
"""
