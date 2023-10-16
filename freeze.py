#!/bin/env python3

import argparse
from ase.io import read, write
from ase.constraints import FixAtoms


def freeze_atoms():
    parser = argparse.ArgumentParser(description="Freeze atoms using ASE")

    parser.add_argument("file", type=str, help="Structure file", required=True)
    parser.add_argument(
        "-i", "--indices", type=int, nargs="+", help="Atom indices to freeze"
    )
    parser.add_argument("-t", "--type", type=str, help="Atom type to freeze")
    parser.add_argument("-z", "--zmax", type=float, help="Freeze atoms with z < zmax")
    parser.add_argument(
        "-o", "--output", type=str, help="Output file name"
    )
    # sort atoms
    parser.add_argument("--sort", action="store_true", help="Sort atoms")
    parser.add_argument(
        "--intersection",
        action="store_true",
        help="Freeze atoms that satisfy all conditions",
    )

    args = parser.parse_args()
    atoms = read(args.file)

    if args.type:
        indices = [i for i, atom in enumerate(atoms) if atom.symbol == args.type]

    if args.zmax:
        indices = [i for i, atom in enumerate(atoms) if atom.position[2] < args.zmax]

    atoms.set_constraint(FixAtoms(indices=indices))
    
    if args.output:
        write(args.output, atoms, vasp5=True, sort=args.sort)

    else: 
        print(atoms)


if __name__ == "__main__":
    freeze_atoms()
