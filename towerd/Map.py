"""
Map class
Used to represent the path for mob troops
Built through an adjacency list representation containing each node with
- id
- type
- coordinates
- edge
"""
import enum


class PathType(enum.Enum):
    PATH_START = 0
    PATH_END = 1
    PATH = 2
    TOWER = 3


class MapNode:
    __ID = 0

    def __init__(self, pathType, x, y):
        """
        Default constructor initializes a node with next available ID
        (starts with initial ID 0)
        """
        # Update Node's ID
        self.id = MapNode.__ID
        self.x = x
        self.y = y
        self.pathType = pathType
        MapNode.__ID = MapNode.__ID + 1

    def __str__(self):
        """
        To string method for node class
        :return: ID # of object
        """
        return f'ID: {self.id}'


class Map:
    """
    A graph representation of the game map.
    :param map_json: a structure read from json
    """
    def __init__(self, map_json=None):
        if map_json:
            self.map = self._generateMapFromJSON(map_json)
        else:
            self.map = {}
        self.nodes = {}

    def _generateMapFromJSON(self, map_json):
        pass

    def __str__(self):
        """
        To String method to display the map
        :return: Returns a string displaying all nodes located within the map
        """
        s = []
        for node, edges in self.map:
            s.append(f'{node} | Type: {node.pathType} | Coordinates: ({node.x}, {node.y}) | Edges: {edges}')
        return '\n'.join(s)

    def addNode(self, pathType, x, y):
        """
        Add a note to map list
        :param pathType: type of node
                        path_start: where mobs appear
                        path_end: end where mob deals damage to player
                        path: normal travel path
                        tower: where a tower can be placed
        :param x: where node is located in x axis (range of [0, 1])
        :param y: where node is located in y axis (range of [0, 1])
        :param edges: adjacent nodes
        """
        n = MapNode(pathType, x, y)
        self.map[n.id] = []
        self.nodes[n.id] = n
        return n

    def addEdge(self, node, target):
        """
        Add a directed edge between two nodes.
        :param node: The starting node or node id
        :param target: The end node or node id
        """
        node = node.id if isinstance(node, MapNode) else node
        target = target.id if isinstance(target, MapNode) else target
        if target not in self.map[node]:
            self.map[node].append(target)

    def existsEdge(self, node, target):
        """
        Check if a directed edge exists between two nodes.
        :param node: The starting node or node id
        :param target: The end node or node id
        """
        node = node.id if isinstance(node, MapNode) else node
        target = target.id if isinstance(target, MapNode) else target
        return target in self.map[node]

    def getMap(self):
        """
        Method to retrieve adjacency list containing map
        :return: map of nodes sub information about node
        """
        return self.map
