"""Módulo para visualização da estrutura"""
import pyvista as pv
import vtk

# pylint: disable=E1101
vtk.vtkObject.GlobalWarningDisplayOff()

# configurações de tema
pv.set_plot_theme('dark')

# Cena
plotter = pv.Plotter()
plotter.camera.parallel_projection = True # Projeção ortográfica
plotter.background_color = '#1a1a1a' # Cor de fundo
plotter.enable_terrain_style(mouse_wheel_zooms=True) # Orbit com o limite no topo
plotter.camera.view_up = (0, 0, 1) # Eixo "z" para cima
plotter.add_axes() # Visualização do eixos globais

# Visualização
plotter.camera_position = [
    (100, -100, 100),  # posição da câmera (x, y, z)
    (0, 0, 0),     # ponto focal (olhando pro centro da cena)
    (0, 0, 1)      # view-up (o eixo Z é o "cima" da tela)
]

# Grid
cell_plane = pv.Plane(i_size=10, j_size=10, i_resolution=100, j_resolution=100)
cell_grid = cell_plane.extract_all_edges()
plotter.add_mesh(cell_grid, show_edges=True, color='#4d4d4d', line_width=1)
section_plane = pv.Plane(i_size=10, j_size=10, i_resolution=10, j_resolution=10)
section_grid = section_plane.extract_all_edges()
plotter.add_mesh(section_grid, show_edges=True, color='#4d4d4d', line_width=3)

# Adiciona qualquer malha ou ator que você queira visualizar
cube = pv.Cube()
plotter.add_mesh(cube)



# Iniciar o loop de interação
plotter.show()
