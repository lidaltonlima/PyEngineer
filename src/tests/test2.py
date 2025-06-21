import pyvista as pv
import numpy as np
import vtk

# Número de pontos
n = 10
pontos = np.random.rand(n, 3) * 10
cloud = pv.PolyData(pontos)

# Cores iniciais
cloud["colors"] = np.full((n, 3), [1.0, 1.0, 1.0])  # Branco

plotter = pv.Plotter()
actor = plotter.add_points(cloud, scalars="colors", rgb=True, point_size=15)

# Picker VTK para identificar o ponto sob o mouse
picker = vtk.vtkPointPicker()
plotter.iren.SetPicker(picker)

# Estado de destaque
ultimo_id = [-1]

# Função de hover
def ao_mover_mouse(obj, event):
    pos = plotter.iren.GetEventPosition()
    picker.Pick(pos[0], pos[1], 0, plotter.renderer)
    point_id = picker.GetPointId()

    if point_id != -1:
        if point_id != ultimo_id[0]:
            # Restaura o último
            if 0 <= ultimo_id[0] < n:
                cloud["colors"][ultimo_id[0]] = [1.0, 1.0, 1.0]  # Branco

            # Destaca o novo
            cloud["colors"][point_id] = [1.0, 0.0, 0.0]  # Vermelho
            ultimo_id[0] = point_id
            actor.GetMapper().GetInput().GetPointData().SetScalars(pv.pyvista_ndarray(cloud["colors"]))
            plotter.render()
    else:
        if 0 <= ultimo_id[0] < n:
            cloud["colors"][ultimo_id[0]] = [1.0, 1.0, 1.0]  # Branco
            ultimo_id[0] = -1
            actor.GetMapper().GetInput().GetPointData().SetScalars(pv.pyvista_ndarray(cloud["colors"]))
            plotter.render()

# Conecta o evento de movimento do mouse
plotter.iren.AddObserver("MouseMoveEvent", ao_mover_mouse)

plotter.show()
