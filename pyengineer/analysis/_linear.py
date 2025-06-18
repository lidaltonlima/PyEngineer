"""Faz a análise linear da estrutura"""
import numpy as np

from .._node import Node
from .._bar import Bar
from .._load import Load
from .._support import Support

class Linear:
    """Análise linear"""
    def __init__(self, nodes: list[Node], bars: list[Bar],
                 loads: list[Load], supports: Support):
        """Construtor

        Args:
            nodes (list[Node]): nós
            bars (list[Bar]): barras
            loads (list[Load]): casos de carga
            supports (Support): apoios
        """
        self.nodes = nodes
        self.bars = bars
        self.loads = loads
        self.supports = supports
        self.matrix_order = 6 * len(nodes)
        self.calculated = False
        self.displacements = None
        self.reactions = None
        self.kg = None
        self.kg_solution = None
        self.forces_vector = None


    def calculate_structure(self):
        """Realiza a calculo"""
        self.displacements = dict()
        self.reactions = dict()
        self.kg_solution = self.calculate_kg_solution()
        self.forces_vector = self.calculate_forces_vector()

        for load in self.loads:
            # Calculate displacements
            self.displacements[load] = np.linalg.inv(self.kg_solution) @ self.forces_vector[load]

            # Calculate reactions
            self.reactions[load] = self.kg @ self.displacements[load] - self.forces_vector[load]

        self.calculated = True


    def calculate_forces_vector(self):
        """Calcula o vetor de forças para cada caso de carga e cria um dicionário

        Returns:
            dict: vetor de forças
        """
        forces = {}
        for load in self.loads:
            f_load = np.zeros(self.matrix_order)

            for node in load.nodes_loads:
                node_position = (self.nodes.index(node) + 1) * 6 - 6

                for force in load.nodes_loads[node].values():
                    for index in range(6):
                        f_load[node_position + index] += force[index]

            forces[load] = f_load.copy()

        return forces


    def calculate_kg(self):
        """ Calcula a matriz de rigidez global

        Returns:
            ndarray: _description_
        """
        kg = np.zeros([self.matrix_order, self.matrix_order])

        for bar in self.bars:
            spread_vector = self.calculate_spread_vector(bar)
            bar.klg = self.calculate_klg(bar)

            line_local = -1 # Índice da linha localmente
            for line_global in spread_vector:
                line_local += 1
                column_local = -1 # Índice da coluna localmente
                for column_global in spread_vector:
                    column_local += 1
                    kg[line_global][column_global] += bar.klg[line_local][column_local]

        return kg


    def calculate_kl(self, bar: Bar):
        """Calcula a matriz de rigidez local da barra

        Args:
            bar (Bar): Barra

        Returns:
            ndarray: matriz de rigidez local
        """
        kl = np.zeros([12, 12])

        l = bar.length
        a = bar.section.area
        ix = bar.section.ix
        iy = bar.section.iy
        iz = bar.section.iz
        e = bar.material.e
        g = bar.material.g

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
        kl[3][3] = (g * ix) / l
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

        bar.kl = kl # Atribui ao objeto

        return kl


    def calculate_klg(self, bar: Bar):
        """Transforma a matriz de rigidez local e global

        Args:
            bar (Bar): _description_

        Returns:
            _type_: _description_
        """
        r = self.calculate_r(bar)
        klg = r.T @ self.calculate_kl(bar) @ r

        bar.klg = klg # Atribui ao objeto

        return klg


    def calculate_kg_solution(self):
        """Aplica os apoios na matriz

        Returns:
            ndarray: matriz de rigidez com os apoios aplicados
        """
        self.kg = self.calculate_kg()
        kg_solution = self.kg.copy()

        for node in self.supports.nodes_support:
            # Índices globais de cada nó
            node_index = self.nodes.index(node)

            index_support = list()
            index = 0
            for support in self.supports.nodes_support[node]:
                if support:
                    index_support.append(6 * (node_index + 1) - (6 - index))

                index += 1


            # Colocar número grande na diagonal
            for i in index_support:
                for j in index_support:
                    if i == j:
                        kg_solution[i][j] = 1e25

        return kg_solution


    def calculate_r(self, bar: Bar):
        """Calcula a matriz de rotação da barra

        Args:
            bar (Bar): barra

        Returns:
            ndarray: matriz de rotação
        """
        x1 = bar.end_node.x
        y1 = bar.end_node.y
        z1 = bar.end_node.z

        dx = bar.dx
        dy = bar.dy
        dz = bar.dz

        rot_aux = np.zeros([3, 3])
        rot_aux[0, 0] = dx / bar.length
        rot_aux[0, 1] = dy / bar.length
        rot_aux[0, 2] = dz / bar.length

        # Ponto auxiliar para determinar o plano "xy" da barra
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

        bar.r = rotation # Atribui matriz de rotação à no objeto barra

        return rotation

    def calculate_spread_vector(self, bar: Bar):
        """Calcula o vetor de espalhamento

        Args:
            bar (Bar): barra

        Returns:
            ndarray: vetor de espalhamento
        """
# Vetor de espalhamento ***************************************************************************
        ni = self.nodes.index(bar.start_node) # Índice do nó inicial
        nf = self.nodes.index(bar.end_node) # Índice do nó final

        spread_vector = [6 * (ni + 1) - 6, 6 * (ni + 1) - 5, 6 * (ni + 1) - 4,
                         6 * (ni + 1) - 3, 6 * (ni + 1) - 2, 6 * (ni + 1) - 1,
                         6 * (nf + 1) - 6, 6 * (nf + 1) - 5, 6 * (nf + 1) - 4,
                         6 * (nf + 1) - 3, 6 * (nf + 1) - 2, 6 * (nf + 1) - 1]
        return spread_vector


    def get_displacements(self, node_name: str, load_name: str):
        """Pega os deslocamentos

        Args:
            node_name (str): mome do nó
            load_name (str): nome da carga

        Returns:
            ndarray: deslocamentos
        """
        for load in self.loads:
            if load.name == load_name:
                for node in self.nodes:
                    if node.name == node_name:
                        node_index = self.nodes.index(node) # Node index
                        initial_index = 6 * (node_index + 1) - 6
                        end_index = 6 * (node_index + 1)

                        node_displacements = self.displacements[load][initial_index : end_index]
                        break
                break

        return node_displacements


    def get_reactions(self, node_name: str, load_name: str):
        """Pega as reações

        Args:
            node_name (str): nome do nó
            load_name (str): nome da carga

        Returns:
            ndarray: reações
        """
        for load in self.loads:
            if load.name == load_name:
                for node in self.nodes:
                    if node.name == node_name:
                        node_index = self.nodes.index(node) # Node index
                        initial_index = 6 * (node_index + 1) - 6
                        end_index = 6 * (node_index + 1)

                        node_reactions = self.reactions[load][initial_index : end_index]
                        break
                break

        return node_reactions
