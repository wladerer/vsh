from pymatgen.io.vasp.outputs import Vasprun
from ifermi.surface import FermiSurface
from ifermi.interpolate import FourierInterpolator
from ifermi.plot import FermiSlicePlotter, FermiSurfacePlotter, save_plot, show_plot
from ifermi.kpoints import kpoints_from_bandstructure
import numpy as np  

def load_surface_info(file: str = 'vasprun.xml', wigner: bool = False, mu: float = 0.0) -> FermiSurface:
    vr = Vasprun(file)
    bs = vr.get_band_structure()

    # interpolate the energies onto a dense k-point mesh
    interpolator = FourierInterpolator(bs)
    dense_bs, velocities = interpolator.interpolate_bands(return_velocities=True)

    # generate the Fermi surface and calculate the dimensionality
    fs = FermiSurface.from_band_structure(
      dense_bs, mu=0.0, wigner_seitz=wigner, calculate_dimensionality=True
    )
    return fs


def make_slice_plots(fermi_surface : FermiSurface, planes: list[int], distances: list[float], hide_cell: bool = True):
    
    #if planes is a single array, make it a list
    if type(planes[0]) == int:
        planes = [planes]

    for plane in planes:
        for i,distance in enumerate(distances):
            slice = fermi_surface.get_fermi_slice((plane[0], plane[1], plane[2]), distance = distance)
            slice_plotter = FermiSlicePlotter(slice)
            plot = slice_plotter.get_plot(hide_cell=hide_cell)
            save_plot(plot, f'{i}_fermi_{plane[1]}{plane[1]}{plane[1]}_{distance}.png')  # saves the plot to a file

    return None

def make_surface_plot(fermi_surface : FermiSurface, hide_cell: bool = True):
    surface_plotter = FermiSurfacePlotter(fermi_surface)
    plot = surface_plotter.get_plot(hide_cell=hide_cell)
    save_plot(plot, f'fermi-surface.png')  # saves the plot to a file

    return None


#make a numpy array that goes from 0 to 0.6 in steps of 0.05
distances = np.arange(0, 0.6, 0.05)
# mus = np.arange(-0.5, 0.5, 0.05)

planes = [ [1, 1, 1] ]
nowig = load_surface_info(file = 'vasprun.xml', wigner = False, mu = 0.0)
make_surface_plot(nowig, hide_cell = False)
make_slice_plots(nowig, planes, distances, hide_cell = False)


