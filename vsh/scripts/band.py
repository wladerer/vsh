#!/usr/bin/env python3

import pyprocar
from ase.io import read

orbital_dict = {
    "s": 0,
    "p_y": 1,
    "p_z": 2,
    "p_x": 3,
    "d_xy": 4,
    "d_yz": 5,
    "d_z2": 6,
    "d_xz": 7,
    "d_x2-y2": 8,
    "f_y(3x2 -y2)": 9,
    "f_xyz": 10,
    "f_yz2": 11,
    "f_z3": 12,
    "f_xz2": 13,
    "f_z(x2 -y2)": 14,
    "f_x(x2 -3y2)": 15,
}


def handle_orbitals(orbitals: list | str) -> list[int]:
    """Converts a string to a list of orbitals"""

    orbital_list = None

    if orbitals is None:
        return None

    # if orbitals is a list of ints, return it
    elif isinstance(orbitals, list) and all(
        isinstance(orbital, int) for orbital in orbitals
    ):
        return orbitals

    elif "all" in orbitals:
        orbital_list = list(range(16))

    elif "s" in orbitals:
        orbital_list = [0]

    elif "p" in orbitals:
        orbital_list = [1, 2, 3]

    elif "d" in orbitals:
        orbital_list = [4, 5, 6, 7, 8]

    elif "f" in orbitals:
        orbital_list = [9, 10, 11, 12, 13, 14, 15]

    elif "xy" in orbitals:
        orbital_list = [1, 3, 4, 8]

    elif "z" in orbitals:
        orbital_list = [2, 6, 12]

    # if orbitals is a string, convert to indices
    elif isinstance(orbitals, str):
        orbital_list = [orbital_dict[orbitals]]

    return orbital_list


def handle_atoms(poscar: str = "./POSCAR") -> dict:
    """Gets identities and indices of atoms from a POSCAR or CONTCAR file"""

    atoms = read(poscar)

    # get list of atom types
    atom_types = atoms.get_chemical_symbols()

    # get dictionary of atom types and indices
    atom_indices = {}
    for i, atom in enumerate(atom_types):
        if atom not in atom_indices:
            atom_indices[atom] = []
        atom_indices[atom].append(i)

    return atom_indices


def plot_procar(args):
    """Plots the band structure from a  file"""

    args.orbitals = handle_orbitals(args.orbitals)

    fig, ax = pyprocar.bandsplot(
        code=args.code,
        mode=args.mode,
        dirname=args.dirname,
        orbitals=args.orbitals,
        atoms=args.atoms,
        spins=args.spins,
        cmap=args.cmap,
        clim=args.clim,
        elimit=args.elimit,
        fermi=args.fermi,
        show=args.output is None,
    )

    if args.output:
        fig.savefig(args.output, dpi=args.dpi)

    return fig, ax


def filter_procar(args):
    """Filters procar file based on user input"""

    pyprocar.filter(args.input, args.output, bands=[584, 652])


def run(args):
    functions = {"plot": plot_procar, "filter": filter_procar}

    functions[args.function](args)
