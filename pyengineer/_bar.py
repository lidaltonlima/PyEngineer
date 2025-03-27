import numpy as np

from ._material import Material
from ._node import Node
from ._section import Section

class Bar:
    def __init__(self, name: str, start_node: Node, end_node: Node, section: Section, material: Material):
        self.name = name
        self.start_node = start_node
        self.end_node = end_node
        self.dx = end_node.x - start_node.x
        self.dy = end_node.y - start_node.y
        self.dz = end_node.z - start_node.z
        self.length = np.sqrt(self.dx**2 + self.dy**2 + self.dz**2)
        self.section = section
        self.material = material
        
    def klg(self):
        return self.r().T @ self.kl() @ self.r()
    
    def kl(self):
        kl = np.zeros([12, 12])
             
        l = self.length
        a = self.section.area
        iy = self.section.iy
        iz = self.section.iz
        j = self.section.j
        e = self.material.e
        g = self.material.g
        
        kl[0][0] = (e * a) / l
        kl[0][6] = -kl[0][0]
        kl[1][1] = (12 * e * iz) / l**3
        kl[1][5] = (6 * e * iz) / l**2
        kl[1][7] = -kl[1][1]
        kl[1][11] = kl[1][5]
        kl[2][2] = (12 * e * iy) / l**3
        kl[2][4] = (-6 * e * iy) / l**2
        kl[2][8] = -kl[2][2]
        kl[2][10] = kl[2][4]
        kl[3][3] = (g * j) / l
        kl[3][9] = -kl[3][3]
        kl[4][4] = (4 * e * iy) / l
        kl[4][8] = -kl[2][4]
        kl[4][10] = (2 * e * iy) / l
        kl[5][5] = (4 * e * iz) / l
        kl[5][7] = -kl[1][5]
        kl[5][11] = (2 * e * iz) / l
        kl[6][6] = kl[0][0]
        kl[7][7] = kl[1][1]
        kl[7][11] = -kl[1][5]
        kl[8][8] = kl[2][2]
        kl[8][10] = -kl[2][4]
        kl[9][9] = kl[3][3]
        kl[10][10] = kl[4][4]
        kl[11][11] = kl[5][5]
        kl = kl + kl.T - np.diag(kl.diagonal())
        
        return kl
    
    def r(self):
        x1 = self.end_node.x
        y1 = self.end_node.y
        z1 = self.end_node.z
        
        dx = self.dx
        dy = self.dy
        dz = self.dz
        
        rot_aux = np.zeros([3, 3])
        rot_aux[0, 0] = dx / self.length
        rot_aux[0, 1] = dy / self.length
        rot_aux[0, 2] = dz / self.length

        # Ponto axiliar para determinar o plano "xy" da barra
        if dx != 0 or dz != 0:
            aux = np.array([x1, y1 + 1, z1])
        else:
            aux = np.array([x1 + 1, y1, z1])
        
        dx = aux[0] - x1
        dy = aux[1] - y1
        dz = aux[2] - z1
        c = np.sqrt(dx**2 + dy**2 + dz**2)
        
        alpha = dx / c
        beta = dy / c
        gamma = dz / c
        
        dx = rot_aux[0, 1] * gamma - rot_aux[0, 2] * beta
        dy = rot_aux[0, 2] * alpha - rot_aux[0, 0] * gamma
        dz = rot_aux[0, 0] * beta - rot_aux[0, 1] * alpha
        c = np.sqrt(dx**2 + dy**2 + dz**2)
        
        rot_aux[2, 0] = dx / c
        rot_aux[2, 1] = dy / c
        rot_aux[2, 2] = dz / c
        
        rot_aux[1, 0] = rot_aux[0, 2] * rot_aux[2, 1] - rot_aux[0, 1] * rot_aux[2, 2]
        rot_aux[1, 1] = rot_aux[0, 0] * rot_aux[2, 2] - rot_aux[0, 2] * rot_aux[2, 0]
        rot_aux[1, 2] = rot_aux[0, 1] * rot_aux[2, 0] - rot_aux[0, 0] * rot_aux[2, 1]
        
        rotation = np.zeros([12, 12])

        rotation[0:3, 0:3] = rot_aux
        rotation[3:6, 3:6] = rot_aux
        rotation[6:9, 6:9] = rot_aux
        rotation[9:12, 9:12] = rot_aux
        
        return rotation

