"""Module for manage nodes and his connection with arrows"""

# Global variables ------------------------------------------------------------

X_RADIUS = 27
Y_RADIUS = 18
Y_LABEL = -3.7

# Classes ---------------------------------------------------------------------

class Node():
    """Class for represent a node with
    his name, if his poisoned and his
    coordinate for display it"""
    def __init__(self, id_node, poisoned, coord):
        self.id_node = id_node
        self.poisoned = poisoned
        self.coord = coord
        self.radius = (X_RADIUS, Y_RADIUS)
        self.label = Y_LABEL
        self.edges = list()

    def set_edges(self, edge):
        """Creates differents edges for
        the node"""
        self.edges.append(edge)

    def __repr__(self):
        return "Node :\n\tID : {}\n\tPoisoned : {}\n\tCoord : {}\n\
        Edges : {}\n".format(self.id_node, self.poisoned, self.coord, self.edges)

    def __del__(self):
        pass
        # print("Node ID {} has been deleted".format(self.id_node))

class CoordN():
    """docstring for Coord_N
    Don't need it for moment delete
    it if never used"""
    def __init__(self, coord, coord_radius, y_label):
        self.coord = coord
        self.coord_radius = coord_radius
        self.y_label = y_label

    def __repr__(self):
        return "CoordN :\n\tCoord : {}\n\tCoord_radius : {}\n\t \
            Label : {}\n".format(self.coord, self.coord_radius, self.y_label)

    def __del__(self):
        print("Coord {} deleted".format(self.coord))

class Arrow():
    """Class for represent an arrow with
    his name and his
    coordinate for display it"""
    def __init__(self, id_arrow, points_line, points_sting):
        self.id_arrow = id_arrow
        self.points_line = points_line
        self.points_sting = points_sting

    def __repr__(self):
        return "Arrow :\n\tID : {}\n\tPoints line : {}\n\
        Points sting : {}\n".format(self.id_arrow, self.points_line, self.points_sting)

    def __del__(self):
        pass
        # print("Arrrow ID {} has been deleted".format(self.id_arrow))

# Functions -------------------------------------------------------------------

def noMorePoisonedNodes(nodes):
	"""verif if there are no more poisoned nodes in the dict"""
	noMore = True
	for node in nodes.values():
		if(node.poisoned):
			noMore = False
			break
	return noMore
	

def delete_node(nodes, id_node_to_delete):
    """Get the nodes dict and the node to delete and
    the other accessible node from him and return the new dict"""
    accessible_nodes = __append_accessible_node(nodes, [id_node_to_delete])
    for id_node in accessible_nodes:
        del nodes[str(id_node)]
    for node in nodes.values():
        for id_node in accessible_nodes:
            if id_node in node.edges:
                node.edges.remove(id_node)

def __append_accessible_node(nodes, id_nodes):
    for id_node in id_nodes:
        for edge in nodes[str(id_node)].edges:
            if edge not in id_nodes:
                id_nodes.append(edge)
                __append_accessible_node(nodes, id_nodes)
    return id_nodes

def initialize_edges(nodes, arrows):
    """Analyze arrows id for create edges
    for each nodes"""
    for arrow in arrows:
        nodes[arrow.id_arrow[0]].set_edges(arrow.id_arrow[1])