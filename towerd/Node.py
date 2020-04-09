"""
Node class used to represent a node within adj list in map class

"""


class Node:
    __ID = 0

    def __init__(self):
        """
        Default constructor initializes a node with next available ID
        (starts with initial ID)
        """

        self.id = Node.__ID
        Node.__ID = Node.__ID + 1

    def __str__(self):
        return f'ID: {self.id}'


n1 = Node()
n2 = Node()
n3 = Node()

print(f'{n1}\n{n2}\n{n3}')