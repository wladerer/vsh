#!/usr/bin/env python3
from ase.io import read, write
from ase.atoms import Atoms
from ase.constraints import FixAtoms

def delete_atoms_by_index(atoms: Atoms, indices: list[int]) -> None:
    '''
    Deletes atoms from a structure
    '''
    del atoms[indices]


def delete_atoms_by_type(atoms: Atoms, types: list[str]) -> None:
    '''
    Deletes atoms from a structure
    '''
    del atoms[[atom.index for atom in atoms if atom.symbol in types]]



def calculate_vacuum(atoms: Atoms) -> float:
    """Subtracts vacuum from a structure"""
    # get z positions
    z_positions = [atom.position[2] for atom in atoms]

    # get max and min z positions
    zmax = max(z_positions)
    zmin = min(z_positions)

    # get c vector
    c = atoms.cell[2][2]

    vacuum = c - zmax

    return vacuum

def freeze_atoms(atoms: Atoms, indices: list[int]) -> None:
    """Freezes atoms in a structure"""
    atoms.set_constraint(FixAtoms(indices=indices))

def freeze_atoms_by_type(atoms: Atoms, types: list[str]) -> None:
    """Freezes atoms in a structure"""
    atoms.set_constraint(FixAtoms(indices=[atom.index for atom in atoms if atom.symbol in types]))

def freeze_atoms_by_z(atoms: Atoms, z: float, direction: str = 'above') -> None:
    """Freezes atoms in a structure"""
    if direction == 'above':
        atoms.set_constraint(FixAtoms(indices=[atom.index for atom in atoms if atom.position[2] > z]))
    elif direction == 'below':
        atoms.set_constraint(FixAtoms(indices=[atom.index for atom in atoms if atom.position[2] < z]))
    else:
        raise ValueError('direction must be "above" or "below"')
    
def freeze_range(atoms: Atoms, zmin: float, zmax: float) -> None:
    """Freezes atoms in a structure"""
    atoms.set_constraint(FixAtoms(indices=[atom.index for atom in atoms if atom.position[2] > zmin and atom.position[2] < zmax]))

def delete_atoms(args):
    """Deletes atoms from a structure"""
    atoms = read(args.input)

    if args.index:
        delete_atoms_by_index(atoms, args.index)
    elif args.type:
        delete_atoms_by_type(atoms, args.type)
    else:
        raise ValueError('Must specify index or type')

    atoms[atoms.numbers.argsort()]

    if not args.output:
        write('-', atoms, format='vasp')
    else:
        write(args.output, atoms, format='vasp')

    return None

def freeze_atoms(args):
    """Freezes atoms in a structure"""
    atoms = read(args.input)

    if args.index:
        freeze_atoms(atoms, args.index)
    elif args.type:
        freeze_atoms_by_type(atoms, args.type)
    elif args.z:
        freeze_atoms_by_z(atoms, args.z, args.direction)
    elif args.range:
        freeze_range(atoms, args.range[0], args.range[1])
    else:
        raise ValueError('Must specify index, type, z, or range')

    atoms[atoms.numbers.argsort()]

    if not args.output:
        write('-', atoms, format='vasp')
    else:
        write(args.output, atoms)

    return None

def swap_atoms(args):
    '''Exchanges atoms of one type into another'''
    atoms = read(args.input)

    if args.index:
        for index in args.index:
            atoms[index].symbol = args.type[0]
    elif args.type:
        for atom in atoms:
            if atom.symbol in args.type:
                atom.symbol = args.type[0]

    atoms[atoms.numbers.argsort()]
    if not args.output:
        write('-', atoms, format='vasp')
    else:
        write(args.output, atoms)

def rattle_atoms(args):
    '''Rattles atoms using MonteCarloRattleTransformation'''
    from pymatgen.transformations.advanced_transformations import MonteCarloRattleTransformation
    from pymatgen.io.ase import AseAtomsAdaptor
    from pymatgen.core.structure import Structure

    atoms = read(args.input)
    structure = AseAtomsAdaptor.get_structure(atoms)
    rattle = MonteCarloRattleTransformation(0.1, 100)
    structure = rattle.apply_transformation(structure)
    atoms = AseAtomsAdaptor.get_atoms(structure)

    atoms[atoms.numbers.argsort()]
    if not args.output:
        write('-', atoms, format='vasp')
    else:
        write(args.output, atoms)

def run(args):
    functions = {
        "delete" : delete_atoms,
        "freeze" : freeze_atoms,
        "swap" : swap_atoms,
        "rattle" : rattle_atoms
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)

    return None

