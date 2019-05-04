class AST:
    def __init__(self, name):
    	self.name = name
    	self.params = []

    def __str__(self):
        return "AST: " + str(self.params)
