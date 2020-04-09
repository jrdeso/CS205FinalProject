"""
Node class used to represent a node within adj list in map class

"""


class Node:
    __ID = 0

    def __init__(self):
        """
        Default constructor initializes a node with next available ID
        (starts with initial ID 0)
        """
        # Update Node's ID
        self.id = Node.__ID
        Node.__ID = Node.__ID + 1

    def __str__(self):
        """
        To string method for node class
        :return: ID # of object
        """
        return f'ID: {self.id}'



# Sample input
# n1 = Node()
# n2 = Node()
# n3 = Node()
#
# print(f'{n1}\n{n2}\n{n3}')