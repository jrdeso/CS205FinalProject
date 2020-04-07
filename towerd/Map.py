"""
Map class
Used to represent the path for mob troops
Built through an adjacency list representation containing each node with
- id
- type
- coordinates
- edge
"""

"""
Graph work - coordinate system example from https://bradfieldcs.com/algos/graphs/representing-a-graph/
    V0   V1   V2   V3   V4   V5           ADJ List
V0       5               2        |   V0 -> id = V0; adj = {V1:5, V5:2}
V1             4                  |   V1 -> id = V1; adj = {V2:4}
V2                  9             |   V2 -> id = V2; adj = {V3:9}
V3                       7   3    |   V3 -> id = V3; adj = {V4:7, V5:3}
V4  1                             |   V4 -> id = V4; adj = {V0:1}
V5              1        8        |   V5 -> id = V5; adj = {V2:1, V4:8}

Our example will include other parameters defined above
"""


class Map:
    def __init__(self):
        """
        Default constructor initializes map adjacency list
        """
        self.map = []

    def addNode(self, id, type, coordinates, edges):
        """
        Add a note to map list
        :param id: id of node
        :param type: type of node
                        path_start: where mobs appear
                        path_end: end where mob deals damage to player
                        path: normal travel path
                        tower: where a tower can be placed
        :param coordinates: where node is located in x,y system
        :param edges: adjacent nodes
        """
        node = [id, type, coordinates, edges]
        self.map.append(node)