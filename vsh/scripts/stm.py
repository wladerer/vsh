from pymatgen.io.vasp import Chgcar
from pymatgen.io.common import VolumetricData
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation


def get_charge_density_from_chgcar(file: str) -> np.array:
    '''Returns the data from a CHGCAR file'''
    chgcar = Chgcar.from_file(file)
    data = chgcar.data['total']
    dims = chgcar.dim
    structure = chgcar.structure 
    return data, dims, structure


def get_charge_density_from_cube(file: str) -> np.array:
    '''Returns the data from a cube file'''
    cube = VolumetricData.from_cube(file)
    data = cube.data
    dims = cube.dim
    structure = cube.structure
    return data, dims, structure


def charge_density_from_file(file: str) -> np.array:
    '''Returns the data from a CHGCAR or cube file'''
    try:
        return get_charge_density_from_chgcar(file)
    except Exception as e:
        # Handle specific exceptions here
        raise ValueError(f'Error reading charge density from file: {str(e)}')


def plot_charge_density_slice(file: str, height: float, repeat_x: int = 1, repeat_y: int = 1, title: str = 'Charge Density', output: str | None = None) -> None:
    '''Plots a CHGCAR file with repeated images in the x and y directions'''
    data, dims, structure = charge_density_from_file(file)
    
    if height < 0 or height > structure.lattice.c:
        raise ValueError(f'Height {height} is not within the range {structure.lattice.c}')
    
    slice_index = int(height / structure.lattice.c * data.shape[2])
    slice_data = data[:, :, slice_index]
    repeated_data = np.tile(slice_data, (repeat_y, repeat_x))
    z = structure.lattice.c * slice_index / data.shape[2]

    plt.imshow(repeated_data, cmap='Greys_r')
    plt.title(f'{title} (Height: {z:.2f} Å)')
    plt.xlabel(r'x ($\mathrm{\AA}$)')
    plt.ylabel(r'y ($\mathrm{\AA}$)')

    if output:
        plt.savefig(output)
    else:
        plt.show()


def animate_slices(file: str, repeat_x: int = 1, repeat_y: int = 1, title: str = 'Charge Density', output: str | None = None) -> None:
    '''Animates slices of a CHGCAR file'''
    data, dims, structure = charge_density_from_file(file)
    total_length = structure.lattice.c
    repeated_data = np.tile(data, (repeat_y, repeat_x, 1))
    fig, ax = plt.subplots()
    im = ax.imshow(repeated_data[:, :, 0], cmap='Greys_r')
    plt.title(f'{title} (Height: 0.00 Å)')
    plt.xlabel(r'x ($\mathrm{\AA}$)')
    plt.ylabel(r'y ($\mathrm{\AA}$)')

    def animate(i):
        im.set_array(repeated_data[:, :, i])
        plt.title(f'{title} (Height: {total_length * i / data.shape[2]:.2f} Å)')
        return [im]

    ani = animation.FuncAnimation(fig, animate, frames=dims[2], blit=False)
    
    if output:
        ani.save(output, writer='imagemagick', fps=5)
    else:
        plt.show()


def stm(subparsers):
    
    subp_stm = subparsers.add_parser('stm', help='Reads, analyses, and plots STM data from CHGCAR or cube files')
    subp_stm.add_argument('input', help='CHGCAR or cube file')
    subp_stm.add_argument('-H', '--height', help='Height of the slice', type=float)
    subp_stm.add_argument('-D', '--dims', help='Repeat in x and y dimensions', type=int, nargs=2)
    subp_stm.add_argument('-a', '--animate', help='Animate slices', action='store_true')
    subp_stm.add_argument('-p', '--plot', help='Plot charge density slice at a certain height', type=str)
    subp_stm.add_argument('-t', '--title', help='Title of the plot', type=str)
    subp_stm.add_argument('-o', '--output', help='Output file name', type=str)

    args = subp_stm.parse_args()
    if not args.animate and args.height is None:
        subp_stm.error("The '--height' argument is required if '--animate' is not selected.")
        
def run(args):
    
    functions = {
        'slice': plot_charge_density_slice,
        'animate': animate_slices
    }
    
    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)