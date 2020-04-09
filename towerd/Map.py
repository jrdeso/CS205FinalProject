"""
Map class
Used to represent the path for mob troops
Built through an adjacency list representation containing each node with
- id
- type
- coordinates
- edge
"""

import Node

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
        :param coordinates: where node is located in x,y system (range of [0, 1])
        :param edges: adjacent nodes
        """
        node = [id, type, coordinates, edges]
        self.map.append(node)

    def getMap(self):
        """
        Method to retrieve adjacency list containing map
        :return: map of nodes and coordinates
        """
        return self.map

    def getRequestedNode(self, id):
        """
        get details of a requested node based off a searched for ID. Can be used to find details of end node/ start node
        :param id: ID being searched for within the map
        :return: return details of the node (id, type, coordinates, edges)
                    Note: if node DNE return -1
        """
        for i in self.map:
            if id == self.map[i][0]:
                return self.map[i]

        return -1
