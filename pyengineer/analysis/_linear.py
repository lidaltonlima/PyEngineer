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


    def calculate_klg(self, bar: Bar):
        """Transforma a matriz de rigidez local e global

        Args:
            bar (Bar): _description_

        Returns:
            _type_: _description_
        """
        r = bar.r
        klg = r.T @ bar.kl @ r

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

            index_support = []
            index_spring = {}
            index = 0
            for support in self.supports.nodes_support[node]:
                if support:
                    if not isinstance(support, bool):
                        index_spring[6 * (node_index + 1) - (6 - index)] = support
                    index_support.append(6 * (node_index + 1) - (6 - index))

                index += 1


            # Colocar número grande na diagonal
            for i in index_support:
                for j in index_support:
                    if i == j:
                        # Se tiver mola, soma apenas a mola
                        if i in index_spring:
                            kg_solution[i][j] += index_spring[i]
                        else:
                            kg_solution[i][j] += 1e25


        return kg_solution

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
