from ._node import Node

class Support:
    def __init__(self, name: str):
        self.name = name
        self.nodes_support = dict()
    
    
    # def add_node_suport(self, node: Node,
    #                     dx: bool = False, dy: bool = False, dz: bool = False,
    #                     rx: bool = False, ry: bool = False, rz: bool = False,):
    #     if not node.name in self.nodes_support:
    #         self.nodes_support[node.name] = list()
        
    #     self.nodes_support[node.name] = [dx, dy, dz, rx, ry, rz]
    
    
    def add_node_fixed(self, node: Node):
        if not node in self.nodes_support:
            self.nodes_support[node] = list()
            
        self.nodes_support[node] = [True, True, True, True, True, True]
    
    # def add_node_pinned(self, node: Node):  
    #     if not node.name in self.nodes_support:
    #         self.nodes_support[node.name] = list()
            
    #     self.nodes_support[node.name] = [True, True, True, False, False, False]
    
    # def add_node_cantilever_roller_x(self, node: Node):
    #     if not node.name in self.nodes_support:
    #         self.nodes_support[node.name] = list()
            
    #     self.nodes_support[node.name] = [False, True, True, False, False, False]
        
       