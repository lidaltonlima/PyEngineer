import numpy as np
import json

# Configurações de apresentação
np.set_printoptions(formatter={'float_kind': '{: .2e}'.format}, linewidth=200)

# Entrada de dados
with open('./porticos/05/input.json') as file:
    data = json.load(file)
    
# constantes //////////////////////////////////////////////////////////////////////////////////////
MATRIX_ORDER = 6 * len(data['nodes'])

# Matrizes das barrras ////////////////////////////////////////////////////////////////////////////
bars_matrix = list() # Lista com todas as barras e suas matrizes calculadas
for bar in data['bars']:
    bar_matrix = dict()
    
    x0 = data['nodes'][bar['nodes'][0]][0] # Nó inicial - Coordenada "x"
    x1 = data['nodes'][bar['nodes'][1]][0] # Nó final - Coordenada "x"
    y0 = data['nodes'][bar['nodes'][0]][1] # Nó inicial - Coordenada "y"
    y1 = data['nodes'][bar['nodes'][1]][1] # Nó final - Coordenada "y"
    z0 = data['nodes'][bar['nodes'][0]][2] # Nó inicial - Coordenada "z"
    z1 = data['nodes'][bar['nodes'][1]][2] # Nó final - Coordenada "z"
    
    dx = x1 - x0 # Delta "x"
    dy = y1 - y0 # Delta "y"
    dz = z1 - z0 # Delta "z"
    l = np.sqrt(dx**2 + dy**2 + dz**2) # Comprimento da barra
    bar_matrix['length'] = l
  
    a = bar['A'] # Área
    iy = bar['Iy'] # Inércia em y
    iz = bar['Iz'] # Inércia em z
    j = bar['J'] # Inércia em polar
    e = data['materials'][bar['material']]['E'] # Módulo de elasticidade
    g = data['materials'][bar['material']]['G'] # Módulo de elasticidade transversal
    
    # Matriz de rigidez local *********************************************************************    
    
    kl = np.zeros([12, 12])
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
    bar_matrix['kl'] = kl
    
    # matriz de rotação ***************************************************************************
    rotation_aux = np.zeros([3, 3])
    rotation_aux[0, 0] = dx / l
    rotation_aux[0, 1] = dy / l
    rotation_aux[0, 2] = dz / l

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
    
    dx = rotation_aux[0, 1] * gamma - rotation_aux[0, 2] * beta
    dy = rotation_aux[0, 2] * alpha - rotation_aux[0, 0] * gamma
    dz = rotation_aux[0, 0] * beta - rotation_aux[0, 1] * alpha
    c = np.sqrt(dx**2 + dy**2 + dz**2)
    
    rotation_aux[2, 0] = dx / c
    rotation_aux[2, 1] = dy / c
    rotation_aux[2, 2] = dz / c
    
    rotation_aux[1, 0] = rotation_aux[0, 2] * rotation_aux[2, 1] - rotation_aux[0, 1] * rotation_aux[2, 2]
    rotation_aux[1, 1] = rotation_aux[0, 0] * rotation_aux[2, 2] - rotation_aux[0, 2] * rotation_aux[2, 0]
    rotation_aux[1, 2] = rotation_aux[0, 1] * rotation_aux[2, 0] - rotation_aux[0, 0] * rotation_aux[2, 1]
    
    rotation = np.zeros([12, 12])

    rotation[0:3, 0:3] = rotation_aux
    rotation[3:6, 3:6] = rotation_aux
    rotation[6:9, 6:9] = rotation_aux
    rotation[9:12, 9:12] = rotation_aux
    
    bar_matrix['rotation'] = rotation

    klg = rotation.T @ kl @ rotation
    bar_matrix['klg'] = klg
    
    # Vetor de espalhamento **********************************************************************
    ni = bar['nodes'][0] # nó inicial
    nf = bar['nodes'][1] # nó final
    
    bar_matrix['index'] = [6 * (ni + 1) - 6, 6 * (ni + 1) - 5, 6 * (ni + 1) - 4,
                           6 * (ni + 1) - 3, 6 * (ni + 1) - 2, 6 * (ni + 1) - 1,
                           6 * (nf + 1) - 6, 6 * (nf + 1) - 5, 6 * (nf + 1) - 4,
                           6 * (nf + 1) - 3, 6 * (nf + 1) - 2, 6 * (nf + 1) - 1]
    
    # Adicionar barra a lista
    bars_matrix.append(bar_matrix)

# Matrizes globais ////////////////////////////////////////////////////////////////////////////////
# Matriz de rigidez global ************************************************************************
kg = np.zeros((MATRIX_ORDER, MATRIX_ORDER))

for bar in bars_matrix:
    line_local = -1 # Ídice da linha localmente
    for line_global in bar['index']:
        line_local += 1
        column_local = -1 # Índice da coluna localmente
        for column_global in bar['index']:
            column_local += 1
            kg[line_global][column_global] += bar['klg'][line_local][column_local]
            
# Vetor de forças ************************************************************************************
global_forces = np.zeros(MATRIX_ORDER)

# Cargas nodais
for node in data['loads']['nodes']:
    node_position = (int(node) + 1) * 6 - 6
    for index in range(6):
        global_forces[node_position + index] += data['loads']['nodes'][node][index]

# Técnica do númer grande /////////////////////////////////////////////////////////////////////////
global_forces_solution = global_forces.copy()
kg_solution = kg.copy()

for node in data['support']:
    # Índices globais de cada nó
    index_forçes = [6 * (node + 1) - 6, 6 * (node + 1) - 5, 6 * (node + 1) - 4,
                    6 * (node + 1) - 3, 6 * (node + 1) - 2, 6 * (node + 1) - 1] 
    
    # Colocar número na diagonal 
    for i in index_forçes:    
        for j in index_forçes:
            if i == j:
                kg_solution[i][j] = 1e25

# Resultados //////////////////////////////////////////////////////////////////////////////////////
# Deslocamentos
displacements = np.linalg.inv(kg_solution) @ global_forces_solution

# Reações de apoio
reactions = kg @ displacements - global_forces
print(displacements)