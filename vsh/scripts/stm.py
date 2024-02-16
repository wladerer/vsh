import matplotlib.animation as animation
import numpy as np
from matplotlib import pyplot as plt
from pymatgen.io.common import VolumetricData
from pymatgen.io.vasp import Chgcar


def get_charge_density_from_chgcar(file: str) -> np.array:
    """Returns the data from a CHGCAR file"""
    chgcar = Chgcar.from_file(file)
    data = chgcar.data["total"]
    dims = chgcar.dim
    structure = chgcar.structure
    return data, dims, structure


def get_charge_density_from_cube(file: str) -> np.array:
    """Returns the data from a cube file"""
    cube = VolumetricData.from_cube(file)
    data = cube.data
    dims = cube.dim
    structure = cube.structure
    return data, dims, structure


def charge_density_from_file(file: str) -> np.array:
    """Returns the data from a CHGCAR or cube file"""
    try:
        return get_charge_density_from_chgcar(file)
    except Exception as e:
        # Handle specific exceptions here
        raise ValueError(f"Error reading charge density from file: {str(e)}")


def plot_charge_density_slice(
    file: str,
    height: float,
    repeat_x: int = 1,
    repeat_y: int = 1,
    title: str = "Charge Density",
    output: str | None = None,
) -> None:
    """Plots a CHGCAR file with repeated images in the x and y directions"""
    data, _, structure = charge_density_from_file(file)

    try:
        if height < 0 or height > structure.lattice.c:
            raise ValueError(
                f"Invalid height: {height}. Height must be within the range [0, {structure.lattice.c}]."
            )
    except TypeError as e:
        raise TypeError(
            f"Invalid height type: {type(height)}. Please provide a float or int using the '-H' flag."
        ) from e

    slice_index = int(height / structure.lattice.c * data.shape[2])
    slice_data = data[:, :, slice_index]
    repeated_data = np.tile(slice_data, (repeat_y, repeat_x))
    z = structure.lattice.c * slice_index / data.shape[2]

    plt.imshow(repeated_data, cmap="Greys_r")
    plt.title(f"{title} (Height: {z:.2f} Å)")
    plt.xlabel(r"x ($\mathrm{\AA}$)")
    plt.ylabel(r"y ($\mathrm{\AA}$)")

    if output:
        plt.savefig(output)
    else:
        plt.show()


def animate_slices(
    file: str,
    repeat_x: int = 1,
    repeat_y: int = 1,
    title: str = "Charge Density",
    output: str | None = None,
) -> None:
    """Animates slices of a CHGCAR file"""
    data, dims, structure = charge_density_from_file(file)
    total_length = structure.lattice.c
    repeated_data = np.tile(data, (repeat_y, repeat_x, 1))
    fig, ax = plt.subplots()
    im = ax.imshow(repeated_data[:, :, 0], cmap="Greys_r")
    plt.title(f"{title} (Height: 0.00 Å)")
    plt.xlabel(r"x ($\mathrm{\AA}$)")
    plt.ylabel(r"y ($\mathrm{\AA}$)")

    def animate(i):
        im.set_array(repeated_data[:, :, i])
        plt.title(f"{title} (Height: {total_length * i / data.shape[2]:.2f} Å)")
        return [im]

    ani = animation.FuncAnimation(fig, animate, frames=dims[2], blit=False)

    if output:
        ani.save(output, writer="imagemagick", fps=5)
    else:
        plt.show()


def plot_slice(args):
    plot_charge_density_slice(
        args.input, args.height, args.dims[0], args.dims[1], args.title, args.output
    )


def animate(args):
    animate_slices(args.input, args.dims[0], args.dims[1], args.title, args.output)


def run(args):
    functions = {"plot": plot_slice, "animate": animate}

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)
