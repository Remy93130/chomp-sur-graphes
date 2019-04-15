"""Module for parse svg file and return the
position of different elements"""

# Global variables ------------------------------------------------------------

GRAPH_PATH = "../ressources/graphes/"

# Imports ---------------------------------------------------------------------

import os
import random
import xml.etree.ElementTree as ET
from .node import Node, Arrow


# Classes ---------------------------------------------------------------------

class Parser:
    """Class for get node's and arrow's coordinates
    Also give the minimum size for the canvas"""

    def __init__(self, window, path=None):
        self.__select_file(path)
        self.parser = ET.parse(self.path)
        self.root = self.parser.getroot()
        self.window_size = window
        self.graph_width = self.root.attrib['width'].replace('pt', '')
        self.graph_height = self.root.attrib['height'].replace('pt', '')

    def get_nodes(self):
        """Return all nodes in the svg file"""
        nodes = list()
        for child in self.root[0]:
            if 'node' in child.attrib.values():
                for element in child:
                    if 'title' in element.tag:
                        current_name = element.text
                    elif 'ellipse' in element.tag:
                        if element.attrib['fill'] == "none":
                            poisoned = False
                        else:
                            poisoned = True
                        nodes.append(
                            Node(current_name,
                                 poisoned,
                                 (float(element.attrib['cx']),
                                  float(element.attrib['cy']) * -1)))
        return self.__create_dico(nodes)

    def get_arrows(self):
        """Return all edges in the svg file"""
        arrows = list()
        for child in self.root[0]:
            if 'edge' in child.attrib.values():
                current_points_line = list()
                for element in child:
                    if 'title' in element.tag:
                        current_name = tuple(element.text.split("->"))
                    elif 'path' in element.tag:
                        element.attrib['d'] = element.attrib['d'].replace('C', ' ')
                        coord_lines = element.attrib['d'].split(' ')
                        coord_lines[0] = coord_lines[0].replace('M', '')
                        coord_lines = coord_lines[::3]
                        for points in coord_lines:
                            points = points.split(',')
                            for point in points:
                                current_points_line.append(point)
                    elif 'polygon' in element.tag:
                        current_points_sting = element.attrib['points'].replace(" ", ",").split(",")
                        self.__formalize_number(current_points_line, current_points_sting)
                        arrows.append(
                            Arrow(current_name,
                                  current_points_line,
                                  current_points_sting))
        return arrows

    def __formalize_number(self, line, sting):
        """Convert negative number for avoid weird result on render
        
        Arguments:
            line {List} -- list of point for line
            sting {List} -- list of point for sting
        """
        for i, value in enumerate(line):
            if float(value) < 0:
                line[i] = self.window_size - (-1 * float(value))
        for i, value in enumerate(sting):
            if float(value) < 0:
                sting[i] = self.window_size - (-1 * float(value))

    @staticmethod
    def __create_dico(nodes):
        """Convert the nodes list to a dictionary for improve the
        complexity of the program

        Arguments:
            nodes {List} -- The list to convert

        Returns:
            Dict -- The dictionary
        """
        dic = dict()
        for node in nodes:
            dic[node.id_node] = node
        return dic

    def __select_file(self, file):
        """Select the file to parse data in other word select 
        the graph for play if None select a random file
        
        Arguments:
            file {string} -- the name of the file
        """
        files = os.listdir(GRAPH_PATH)
        if not file:
            selected = GRAPH_PATH + random.choice(files)
        else:
            assert file in files
            selected = GRAPH_PATH + file
        self.path = selected
