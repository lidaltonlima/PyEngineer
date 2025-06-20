"""Módulo para visualização da estrutura"""
import typing as tp
import pyvista as pv
import vtk
from ..analysis import Linear
from .objects import supports

class IStyles(tp.TypedDict):
    """Interface para estilos"""
    theme: str
    background_color: str

    grid_size: float
    cell_size: float
    cell_width: float
    cell_color: str

    section_size: float
    section_width: float
    section_color: str

    node_size: int
    node_color: str
    bar_width: int
    bar_color: str


class Structure:
    """Visualização da estrutura"""
    def __init__(self, analysis: Linear):
        self.analysis = analysis
        self.styles: IStyles = {
            'theme': 'dark',
            'background_color': '#1a1a1a',
            # Grid
            'grid_size': 50,

            'cell_size': 1,
            'cell_width': 1,
            'cell_color': '#4d4d4d',

            'section_size': 10,
            'section_width': 2,
            'section_color': '#4d4d4d',

            # Objetos
            'node_size': 10,
            'node_color': 'blue',
            'bar_width': 3,
            'bar_color': 'orange'
        }
        self.plotter = pv.Plotter()


    def _add_objects(self) -> None:
        # Points //////////////////////////////////////////////////////////////////////////////////
        points_position = []
        for node in self.analysis.nodes:
            points_position.append(node.position)

        self.plotter.add_mesh(pv.PolyData(points_position),
                              color=self.styles['node_color'],
                              point_size=self.styles['node_size'])

        # Bars ////////////////////////////////////////////////////////////////////////////////////
        for bar in self.analysis.bars:
            line = pv.Line(bar.start_node.position, bar.end_node.position)
            self.plotter.add_mesh(line,
                                  color=self.styles['bar_color'],
                                  line_width=self.styles['bar_width'])

        # Apoios //////////////////////////////////////////////////////////////////////////////////
        # Fixo no deslocamento ********************************************************************
        for node, support in self.analysis.supports.nodes_support.items():
            for index, value in enumerate(support):
                if index > 2:
                    break

                match index:
                    case 0:
                        axis = 'x'
                    case 1:
                        axis = 'y'
                    case 2:
                        axis = 'z'

                if isinstance(value, bool) and value:
                    supports.fixed_displacement(self.plotter, node.position, axis)
        # Mola no deslocamento ********************************************************************
        for node, support in self.analysis.supports.nodes_support.items():
            for index, value in enumerate(support):
                if index > 2:
                    break

                match index:
                    case 0:
                        axis = 'x'
                    case 1:
                        axis = 'y'
                    case 2:
                        axis = 'z'

                if isinstance(value, float):
                    supports.spring_displacement(self.plotter, node.position, axis)

        # Fixo na rotação *************************************************************************
        for node, support in self.analysis.supports.nodes_support.items():
            for index, value in enumerate(support):
                if index >= 3:
                    match index:
                        case 3:
                            axis = 'x'
                        case 4:
                            axis = 'y'
                        case 5:
                            axis = 'z'

                    if isinstance(value, bool) and value:
                        supports.fixed_rotation(self.plotter, node.position, axis)
        # Mola na rotação *************************************************************************
        for node, support in self.analysis.supports.nodes_support.items():
            for index, value in enumerate(support):
                if index >= 3:
                    match index:
                        case 3:
                            axis = 'x'
                        case 4:
                            axis = 'y'
                        case 5:
                            axis = 'z'

                    if isinstance(value, float):
                        supports.spring_rotation(self.plotter, node.position, axis)
        # /////////////////////////////////////////////////////////////////////////////////////////


    def _config(self) -> None:
        """Faz as configurações iniciais"""
        # pylint: disable=E1101
        vtk.vtkObject.GlobalWarningDisplayOff() # Desativar erros

        pv.set_plot_theme(self.styles['theme']) # Tema geral

        self.plotter.background_color = self.styles['background_color'] # Cor de fundo
        self.plotter.enable_terrain_style(mouse_wheel_zooms=True) # Orbit com o limite no topo
        self.plotter.camera.view_up = (0, 0, 1) # Eixo "z" para cima
        self.plotter.add_axes() # Visualização do eixos globais

        self.plotter.camera_position = [
            (50, -50, 50),  # posição da câmera (x, y, z)
            (0, 0, 0),     # ponto focal (olhando pro centro da cena)
            (0, 0, 1)      # view-up (o eixo Z é o "cima" da tela)
        ]

        # Grid ////////////////////////////////////////////////////////////////////////////////////
        # Cell ************************************************************************************
        cell_resolution = int(round(self.styles['grid_size'] / self.styles['cell_size'], 0))
        cell_plane = pv.Plane(i_size=self.styles['grid_size'], j_size=self.styles['grid_size'],
                              i_resolution=cell_resolution, j_resolution=cell_resolution)
        cell_grid = cell_plane.extract_all_edges()
        self.plotter.add_mesh(cell_grid,
                              show_edges=True,
                              color=self.styles['cell_color'],
                              line_width=self.styles['cell_width'])

        # Section *********************************************************************************
        section_resolution = int(round(self.styles['grid_size'] / self.styles['section_size'], 0))
        section_plane1 = pv.Plane((0, 0, 0.0001),
                                 i_size=self.styles['grid_size'], j_size=self.styles['grid_size'],
                                 i_resolution=section_resolution, j_resolution=section_resolution)
        section_grid1 = section_plane1.extract_all_edges()
        self.plotter.add_mesh(section_grid1, show_edges=True,
                              color=self.styles['section_color'],
                              line_width=self.styles['section_width'])
        # Parte inferior para ficar sempre na frente do "cell"
        section_plane2 = pv.Plane((0, 0, -0.0001),
                                 i_size=self.styles['grid_size'], j_size=self.styles['grid_size'],
                                 i_resolution=section_resolution, j_resolution=section_resolution)
        section_grid2 = section_plane2.extract_all_edges()
        self.plotter.add_mesh(section_grid2, show_edges=True,
                              color=self.styles['section_color'],
                              line_width=self.styles['section_width'])
        # /////////////////////////////////////////////////////////////////////////////////////////

    def show(self):
        """Inicia a visualização"""
        self._config()
        self._add_objects()
        self.plotter.show()
