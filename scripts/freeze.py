#!/usr/bin/env python3

from ase.io import read, write
from ase.atoms import Atoms
from ase.constraints import FixAtoms

def calculate_vacuum(atoms: Atoms) -> float:
    """Subtracts vacuum from a structure"""
    # get z positions
    z_positions = [atom.position[2] for atom in atoms]

    # get max and min z positions
    zmax = max(z_positions)
    zmin = min(z_positions)

    # get c vector
    c = atoms.cell[2][2]

    vacuum = c - (zmax)

    return vacuum


def run(args):
    atoms = read(args.inputname)

    conditions = {
        "type": lambda atom: atom.symbol == args.type,
        "zmax": lambda atom: atom.position[2] < args.zmax,
        "zrange": lambda atom: args.zrange[0] < atom.position[2] < args.zrange[1],
    }

    for arg, condition in conditions.items():
        if getattr(args, arg):
            args.indices = [i for i, atom in enumerate(atoms) if condition(atom)]

    atoms.set_constraint(FixAtoms(indices=args.indices))

    if args.output:
        write(args.output, atoms, vasp5=True, sort=args.sort)
    else:
        print(atoms)

    return None
