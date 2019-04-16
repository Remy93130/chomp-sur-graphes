#!/usr/bin/python3
#-*- coding: utf-8 -*
"""[summary]
[description]
"""

import random
from graphviz import Digraph, render

class AutomatedNode:
    """Class for create nodes by a generated graph
    """
    def __init__(self, id_node, edge_in, edge_out):
        self.id_node = id_node
        self.edge_in = edge_in
        self.edge_out = edge_out

    def create_node(self):
        """[summary]
        [description]
        """
        return self

    def __repr__(self):
        return "Generated node:\n\tId: {}\n\tEin: {}\n\tEout: {}".format(
            self.id_node, self.edge_in, self.edge_out
            )

class AutomatedGraph:
    """Class for create a graph randomly generated
    Expect work with AutomatedNode.
    """
    def __init__(self, node_max, edge_min, edge_max):
        self.node_max = node_max
        self.edge_min = edge_min
        self.edge_max = edge_max

    def __generate_node(self):
        """Generates nodes for prepare the display
        Returns:
            Dict -- The dictionary of nodes generated
        """
        nodes = dict()
        for i in range(self.node_max):
            edge_in, edge_out = float("Inf"), float("Inf")
            while edge_in > self.node_max or edge_out > self.node_max:
                total_edges = random.randint(self.edge_min, self.edge_max)
                edge_in = random.randint(self.edge_min, total_edges)
                edge_out = self.edge_max - total_edges
            nodes[i] = AutomatedNode(i, edge_in, edge_out)
        return nodes

    def display_graph(self):
        """Create an image of the graph and display it on the user screen
        """
        generated = Digraph(format="svg", engine="sfdp")
        nodes = self.__generate_node()
        poisoned = random.randint(0, self.node_max - 1)
        generated.node(str(poisoned), color="lightblue", style="filled")
        for node in nodes.values():
            edges = set()
            for _i in range(node.edge_out):
                next_node = node.id_node
                while next_node == node.id_node or next_node in edges:
                    next_node = random.randint(0, self.node_max - 1)
                    if next_node == node.id_node or next_node in edges:
                        continue
                    if nodes[next_node].edge_in > 0:
                        nodes[next_node].edge_in -= 1
                        break
                edges.add(next_node)
            for target in edges:
                generated.edge(str(node.id_node), str(target))
        generated.render()
        render("sfdp", "svg", "Digraph.gv")
        generated.view()

    def __repr__(self):
        return "Generated graph:\n\tMax: {}\n\tEmin: {}\n\tEmax: {}".format(
            self.node_max, self.edge_min, self.edge_max
            )

def main():
    """Just a random main"""
    graph = AutomatedGraph(20, 0, 2)
    graph.display_graph()

if __name__ == '__main__':
    main()
