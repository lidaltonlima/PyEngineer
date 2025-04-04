from ._node import Node

class Support:
    def __init__(self, name: str):
        self.name = name
        self.nodes_support = dict()
    
      
    def add_support(self, node: Node, supports: list[bool]):
        if not node in self.nodes_support:
            self.nodes_support[node] = list()
            
        self.nodes_support[node] = supports
    
    
    def add_fixed_support(self, node: Node):
        if not node in self.nodes_support:
            self.nodes_support[node] = list()
            
        self.nodes_support[node] = [True, True, True, True, True, True]
    
    def add_pinned_support(self, node: Node):  
        if not node in self.nodes_support:
            self.nodes_support[node] = list()
            
        self.nodes_support[node] = [True, True, True, False, False, False]
    
    # def add_node_cantilever_roller_x(self, node: Node):
    #     if not node.name in self.nodes_support:
    #         self.nodes_support[node.name] = list()
            
    #     self.nodes_support[node.name] = [False, True, True, False, False, False]
        
       