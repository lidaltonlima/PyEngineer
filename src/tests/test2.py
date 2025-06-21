"""Test"""
import numpy as np
import pyvista as pv

pv.set_plot_theme('dark')
plotter = pv.Plotter()
plotter.enable_terrain_style()

point = np.array([0, 0, 0])
arrow = pv.Arrow((0, 0, 0), (0, 0, -1), scale=2, tip_radius=0.1, shaft_radius=0.03 )
plotter.add_mesh(arrow)
plotter.add_axes_at_origin()
plotter.show()
