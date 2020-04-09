"""
Map class
Used to represent the path for mob troops
Built through an adjacency list representation containing each node with
- id
- type
- coordinates
- edge
"""
from Node import Node


class Map:
    def __init__(self):
        """
        Default constructor initializes map adjacency list
        """
        self.map = dict()

    def addNode(self, type, coordinates, edges):
        """
        Add a note to map list - ID incremented in node class
        :param type: type of node
                        path_start: where mobs appear
                        path_end: end where mob deals damage to player
                        path: normal travel path
                        tower: where a tower can be placed
        :param coordinates: where node is located in x,y system (range of [0, 1])
        :param edges: adjacent nodes
        """
        n = Node()
        self.map[n] = [type, coordinates, edges]

    def getMap(self):
        """
        Method to retrieve adjacency list containing map
        :return: map of nodes and coordinates
        """
        return self.map

    def __str__(self):
        s = ""
        for i in self.map:
            s += str(i) + " | Type: " + str(self.map[i][0]) + " | Coordinates: " + str(self.map[i][1]) + " | Edges: " +\
                 str(self.map[i][2])

        return s


# tests
m = Map()
m.addNode("start", [0, .1], ['a', 'b'])

print(m)
