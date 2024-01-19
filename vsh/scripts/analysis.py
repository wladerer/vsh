#!/usr/bin/env python3

from ase.calculators.vasp import Vasp
from ase.spacegroup import get_spacegroup
from ase import Atoms
from ase.io import read, write
from scipy.spatial.distance import cdist
import numpy as np


def validate_atoms(atoms: Atoms) -> bool:
    """Checks if an atoms object is valid"""
    if not isinstance(atoms, Atoms) or len(atoms) == 0:
        return False
    else:
        return True


def is_diatomic(atoms: Atoms) -> bool:
    """Checks if an atoms object is diatomic"""
    if validate_atoms(atoms) == False:
        raise ValueError("Invalid atoms object")
    if len(atoms) == 2:
        return True
    else:
        return False


def get_adjacency_matrix(atoms: Atoms) -> np.ndarray:
    """Gets the adjacency matrix of a structure"""
    if validate_atoms(atoms) == False:
        raise ValueError("Invalid atoms object")
    # get the positions of the atoms object
    positions = atoms.get_positions()
    adjacency_matrix = cdist(positions, positions)

    return adjacency_matrix


def get_number_of_atoms(atoms: Atoms) -> int:
    """Gets the number of atoms in an atoms object"""
    return len(atoms)


def analyze_adjacency_matrix(adjacency_matrix: np.ndarray, min_dist: float):
    """Checks if the adjacency matrix is reasonable"""
    # update diagonals to be very large
    np.fill_diagonal(adjacency_matrix, 1000)
    # check if any off diagonal is less than min_dist, return the indices of the offending atoms
    indices = np.where(adjacency_matrix < min_dist)

    bond_lengths = adjacency_matrix[indices]
    if len(indices) > 0:
        return indices, bond_lengths
    else:
        return None


def unpack_indices(
    indices: tuple[np.ndarray], element_list: list[str], bond_lengths: np.ndarray
):
    """Returns a dictionary of atom pairs"""
    # check if indices is an empty np array, if so return None
    if any(len(index) < 2 for index in indices) or len(indices) == 0 or indices == None:
        return None

    atom_pairs = {}
    for length, pair in enumerate(indices):
        first_element_index, second_element_index = pair
        first_element = element_list[first_element_index]
        second_element = element_list[second_element_index]
        bond_length = bond_lengths[length]
        entry = {
            f"{first_element}{first_element_index}-{second_element}{second_element_index}": bond_length
        }
        atom_pairs.update(entry)

    return atom_pairs


def conflicting_atoms(atoms: Atoms, min_dist: float) -> dict:
    """Checks if a structure has atoms that are too close together"""
    if is_diatomic(atoms):
        # get length between the two atoms
        positions = atoms.get_positions()
        bond_length = np.linalg.norm(positions[0] - positions[1])
        if bond_length < min_dist:
            return {f"{atoms[0].symbol}{0}-{atoms[1].symbol}{1}": bond_length}
        else:
            return None

    neighbor_list = get_adjacency_matrix(atoms)
    indices, bond_lengths = analyze_adjacency_matrix(neighbor_list, min_dist)
    element_list: tuple[np.ndarray] = atoms.get_chemical_symbols()

    if indices == None or len(indices) == 0:
        return None

    print(indices)
    print(get_number_of_atoms(atoms))
    # check if indices is greater than or equal to the number of atoms
    if len(indices) >= get_number_of_atoms(atoms):
        raise ValueError("Min distance is too large or the structure may be corrupt")

    return unpack_indices(indices, element_list, bond_lengths)


def print_conflicts(conflicts: dict):
    """Prints the conflicting atoms"""
    if conflicts == None:
        print("No conflicting atoms")
    else:
        print("Atom pair Bond length")
        for key, value in conflicts.items():
            print(f"{key} {value}")

    return None


def check_convergence(file: str = "./vasprun.xml") -> list[bool]:
    """Looks for vasprun.xml file and checks if converged"""
    import os

    # import Vasprun from pymatgen
    from pymatgen.io.vasp.outputs import Vasprun

    vasprun_object = Vasprun(file, parse_dos=False, parse_eigen=False, parse_projected_eigen=False, parse_potcar_file=False)
    converged_electronic = vasprun_object.converged_electronic
    converged_ionic = vasprun_object.converged_ionic 

    return [converged_electronic, converged_ionic]


def inspect_oszicar(file: str = "./OSZICAR") -> dict:
    '''Reads an OSZICAR file and returns a dictionary of convergence information'''
    from pymatgen.io.vasp.outputs import Oszicar

    oszicar_object = Oszicar(file)
    return oszicar_object.as_dict()

def get_conflicts(args):
    atoms = read(args.input)
    conflicts = conflicting_atoms(atoms, args.conflicts)
    print_conflicts(conflicts)

def get_volume(args):
    atoms = read(args.input)
    print(atoms.get_volume())

def get_cell(args):
    atoms = read(args.input)
    cell = atoms.get_cell()
    # if anything is less than 0.01, set it to 0
    cell = np.where(np.abs(cell) < 0.01, 0, cell)
    print(f"{cell[0][0]:.5f} {cell[0][1]:.5f} {cell[0][2]:.5f}")
    print(f"{cell[1][0]:.5f} {cell[1][1]:.5f} {cell[1][2]:.5f}")
    print(f"{cell[2][0]:.5f} {cell[2][1]:.5f} {cell[2][2]:.5f}")

def get_params(args):
    atoms = read(args.input)
    cell = atoms.cell.cellpar()
    print(f"a = {cell[0]:.5f}")
    print(f"b = {cell[1]:.5f}")
    print(f"c = {cell[2]:.5f}")

def get_symmetry(args):
    atoms = read(args.input)
    spacegroup = get_spacegroup(atoms)
    print(f"Space group number: {spacegroup.no}")
    print(f"Space group symbol: {spacegroup.symbol}")

def get_vacuum(args):
    atoms = read(args.input)
    z = atoms.cell.cellpar()[2]
    z_coords = atoms.get_positions()[:, 2]
    z_max = np.max(z_coords)
    z_min = np.min(z_coords)
    vacuum = z - (z_max - z_min)
    print(f"Vacuum: {vacuum:.5f}")

def get_energy(args):
    atoms = read(args.input)
    calculator = Vasp(atoms)
    energy = calculator.get_potential_energy()
    print(f"Energy: {energy:.5f}")

def get_converged(args):
    # handle xml.elementree error. this means that the calculation is not finished or the file is corrupt
    try:
        electronic, ionic = check_convergence(args.input)
        print(f"Electronic convergence: {electronic}")
        print(f"Ionic convergence: {ionic}")
    except:
        print("Calculation not finished or file is corrupt")
        exit()

def get_equivalent_positions(pmg_structure):
    """Get the equivalent positions of a structure"""
    from pymatgen.core.structure import Structure
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

    spacegroup = SpacegroupAnalyzer(pmg_structure)
    sym_structure = spacegroup.get_symmetrized_structure()
    sites = sym_structure.equivalent_sites

    for site in sites:
        print(site[0].species_string, site[0].frac_coords)
    
    return None

def run(args):
    functions = {
        "conflicts": get_conflicts,
        "volume": get_volume,
        "cell": get_cell,
        "params": get_params,
        "symmetry": get_symmetry,
        "vacuum": get_vacuum,
        "energy": get_energy,
        "converged": get_converged,
    }
    
    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)