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
        Default constructor initializes map dictionary
        Key = ID
        ID : [type, coordinates, edge nodes]
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
        :return: map of nodes sub information about node
        """
        return self.map

    def __str__(self):
        """
        To String method to display the map
        :return: Returns a string displaying all nodes located within the map
        """
        s = ""
        for i in self.map:
            s += str(i) + " | Type: " + str(self.map[i][0]) + " | Coordinates: " + str(self.map[i][1]) + " | Edges: " +\
                 str(self.map[i][2]) + "\n"

        return s


# Code tests
m = Map()
m.addNode("start", [0, .1], ['a', 'b'])
m.addNode("Path", [.1, .1], ['b', 'c'])
m.addNode("End", [.1, .2], ['c', 'd'])
# Displays all contents of map
print(m)
