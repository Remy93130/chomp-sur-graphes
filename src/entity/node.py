"""Module for manage nodes and his connection with arrows"""

class Node():
    """docstring for Node"""
    def __init__(self, id_node, poisoned, coord):
        self.id_node = id_node
        self.poisoned = poisoned
        self.coord = coord
        self.edges = list()

    def set_edges(self, edges):
        """Creates differents edges for
        the node"""
        for edge in edges:
            self.edges.append(edge)

    def delete_node(self):
        """delete the node and his edges"""
        self.id_node = None
        for edge in self.edges:
            # Wrong edge store only the id_node of the node ?
            edge.delete_node()

    def __str__(self):
        return "Node :\n\tID : {}\n\tPoisoned : {}\n\tCoord : {} \n\t \
            Edges : {}".format(self.id_node, self.poisoned, self.coord, self.edges)

    def __del__(self):
        print("Node ID {} has been deleted".format(self.id_node))

class CoordN():
    """docstring for Coord_N"""
    def __init__(self, coord, coord_radius, y_label):
        self.coord = coord
        self.coord_radius = coord_radius
        self.y_label = y_label

    def __str__(self):
        return "CoordN :\n\tCoord : {}\n\tCoord_radius : {}\n\t \
            Label : {}".format(self.coord, self.coord_radius, self.y_label)

    def __del__(self):
        print("Coord {} deleted".format(self.coord))

class Arrow():
    """docstring for Arrow"""
    def __init__(self, id_arrow, points_line, points_sting):
        self.id_arrow = id_arrow
        self.points_line = points_line
        self.points_sting = points_sting

    def __str__(self):
        return "Arrow :\n\tID : {}\n\tpoints line : {}\n\t \
            Points sting : {}".format(self.id_arrow, self.points_line, self.points_sting)

    def __del__(self):
        print("Arrrow ID {} has been deleted".format(self.id_arrow))
