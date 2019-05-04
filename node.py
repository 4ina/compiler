class Node:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.params = []
    def __str__(self):
        return "Node " + self.type.name + ', ' + self.name + ', ' + str(self.params)
