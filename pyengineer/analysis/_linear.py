from numpy import zeros

from .._node import Node
from .._bar import Bar
from .._load import Load
from .._support import Support

class Linear:
    def __init__(self, nodes: list[Node], bars: list[Bar],
                 loads: list[Load], supports: Support):
        self.nodes = nodes
        self.bars = bars
        self.loads = loads
        self.supports = supports
        self.matrix_order = 6 * len(nodes)
        
    
    def kg(self):
        kg = zeros([self.matrix_order, self.matrix_order])
        
        
        # for bar in bars_matrix:
        #     line_local = -1 # Ídice da linha localmente
        #     for line_global in bar['index']:
        #         line_local += 1
        #         column_local = -1 # Índice da coluna localmente
        #         for column_global in bar['index']:
        #             column_local += 1
        #             kg[line_global][column_global] += bar['klg'][line_local][column_local]
            
        
        
        return kg