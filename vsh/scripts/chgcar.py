from pymatgen.io.vasp import Chgcar


def write_output(chgcar, output, cube):
    if cube:
        chgcar.to_cube(output)
    else:
        chgcar.write_file(output)


def plot_linear_slice(
    file: str,
    point1: list[float, float, float],
    point2: list[float, float, float],
    npoints: int = 100,
):
    """Plots a linear slice of the CHGCAR file."""
    from matplotlib import pyplot as plt
    import numpy as np

    chgcar = Chgcar.from_file(file)
    charge_line = chgcar.linear_slice(
        point1, point2, npoints
    )  # 1d array of values along the slice
    # get fractional coordinates along the slice
    frac_coords = chgcar.structure.lattice.get_fractional_coords(charge_line[0])
    # get the distance along the slice
    dist = np.linalg.norm(charge_line[0] - charge_line[-1])
    # get the distance between each point along the slice
    dists = np.linspace(0, dist, npoints)
    # plot the charge density along the slice
    plt.plot(dists, charge_line)
    plt.xlabel("Distance along slice (Angstroms)")
    plt.ylabel("Charge density (e/Angstrom^3)")
    plt.title("Charge density along slice")
    plt.show()


def run(args):
    try:
        chgcar1 = Chgcar.from_file(args.input[0])
        chgcar = chgcar1  # Initialize chgcar to chgcar1 in case args.sum and args.diff are both False
        if args.sum or args.diff:  # Only try to read the second file if necessary
            chgcar2 = Chgcar.from_file(args.input[1])
    except IndexError:
        print("Error: Not enough input files specified.")
        return
    except FileNotFoundError as e:
        print(f"Error: File not found: {e.filename}")
        return

    if args.sum:
        chgcar += chgcar2
    elif args.diff:
        chgcar -= chgcar2

    if args.output:
        write_output(chgcar, args.output, args.cube)
    else:
        print(chgcar)
