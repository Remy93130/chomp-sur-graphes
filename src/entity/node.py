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
        self.coaccess = list()

    def set_edges(self, edge):
        """Creates differents edges for
        the node
        
        Arguments:
            edge {str} -- The id of the node
        """
        self.edges.append(edge)

    def set_coaccess(self, edge):
        """Creates differents coaccessibles edges for
        the node
        
        Arguments:
            edge {str} -- The id of the node
        """
        self.coaccess.append(edge)

    def __repr__(self):
        return "Node :\n\tID : {}\n\tPoisoned : {}\n\tCoord : {}\n\
        Edges : {}\n".format(self.id_node, self.poisoned, self.coord, self.edges, self.coaccess)

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
	"""Check if there are no more poisoned nodes in the dict
    
    Arguments:
        nodes {Dict} -- The nodes dictionnary
    
    Returns:
        bool -- Boolean to check if still poisoned node
    """
	noMore = True
	for node in nodes.values():
		if(node.poisoned):
			noMore = False
			break
	return noMore
	

def delete_node(nodes, id_node_to_delete):
    """Get the nodes dict and the node to delete and
    the other accessible node from him and return the new dict
    
    Arguments:
        nodes {Dict} -- The node's dictionary
        id_node_to_delete {str} -- The id of the node to delete
    """
    accessible_nodes = __append_accessible_node(nodes, [id_node_to_delete])
    coaccess_nodes = __append_coaccess_node(nodes, [id_node_to_delete])
    for id_node in accessible_nodes:
        del nodes[str(id_node)]
    for node in nodes.values():
        for id_node in accessible_nodes:
            try:
                node.edges.remove(id_node)
            except Exception as e:
                pass
            
        for id_node in coaccess_nodes:
            try:
                node.coaccess.remove(id_node)
            except Exception as e:
                pass

def safe_nodes(nodes):
    """Get the nodes dict and return a list of the safe nodes
    
    Arguments:
        nodes {Dict} -- The node's dictionary
    """
    safe = list()

    for node in nodes.values() :
        if __is_safe([node.id_node], nodes) :
            safe.append(node.id_node)

    return safe

def __append_accessible_node(nodes, id_nodes):
    """Append to the list id_nodes all node to delete
    Recursive function
    
    Arguments:
        nodes {Dict} -- The node's dictionary
        id_nodes {int} -- The id to the node of delete
    
    Returns:
        List -- List of node id to delete
    """
    for id_node in id_nodes:
        for edge in nodes[str(id_node)].edges:
            if edge not in id_nodes:
                id_nodes.append(edge)
                __append_accessible_node(nodes, id_nodes)
    return id_nodes

def __append_coaccess_node(nodes, id_nodes):
    """Append to the list id_nodes all node to delete
    Recursive function
    
    Arguments:
        nodes {Dict} -- The node's dictionary
        id_nodes {int} -- The id to the node of delete
    
    Returns:
        List -- List of node id to delete
    """
    for id_node in id_nodes:
        for edge in nodes[str(id_node)].coaccess:
            if edge not in id_nodes:
                id_nodes.append(edge)
                __append_coaccess_node(nodes, id_nodes)
    return id_nodes

def __is_safe(id_nodes, nodes):
    """Tests if the node is safe based on the nodes' dict
    
    Arguments:
        node -- The node object concerned
        nodes {Dict} -- The node's dictionary
    
    Returns:
        Bool -- True if safe, False the other way
    """
    for id_node in id_nodes:
        if nodes[id_node].poisoned :
            return False
        for edge in nodes[id_node].edges :
            if edge not in id_nodes :
                id_nodes.append(edge)
                if not __is_safe(id_nodes, nodes) :
                    return False
    return True

def initialize_edges(nodes, arrows):
    """Analyze arrows id for create edges
    for each nodes
    
    Arguments:
        nodes {Dict} -- The node's dictionary
        arrows {List} -- The list of arrows
    """
    for arrow in arrows:
        nodes[arrow.id_arrow[0]].set_edges(arrow.id_arrow[1])
        nodes[arrow.id_arrow[1]].set_coaccess(arrow.id_arrow[0])