#!/usr/bin/env python3

import argparse
from ase.io import read, write
from ase.constraints import FixAtoms


def setup_args(subparsers):
    subp_freeze = subparsers.add_parser("freeze", help="Freeze atoms using ASE")

    subp_freeze.add_argument(
        "-i", "--input", type=str, help="Structure file", required=True
    )
    subp_freeze.add_argument(
        "--indices",
        type=int,
        nargs="+",
        default=None,
        help="Atom indices to freeze",
    )
    subp_freeze.add_argument("-t", "--type", type=str, help="Atom type to freeze")
    subp_freeze.add_argument(
        "-z", "--zmax", type=float, help="Freeze atoms with z < zmax"
    )
    subp_freeze.add_argument("-o", "--output", type=str, help="Output file name")
    # sort atoms
    subp_freeze.add_argument("--sort", action="store_true", help="Sort atoms")
    subp_freeze.add_argument(
        "--zrange", type=float, nargs=2, help="Freeze atoms with zmin < z < zmax"
    )


def run(args):
    atoms = read(args.inputname)

    if args.type:
        args.indices = [i for i, atom in enumerate(atoms) if atom.symbol == args.type]

    if args.zmax:
        args.indices = [
            i for i, atom in enumerate(atoms) if atom.position[2] < args.zmax
        ]

    if args.zrange:
        args.indices = [
            i
            for i, atom in enumerate(atoms)
            if args.zrange[0] < atom.position[2] < args.zrange[1]
        ]

    atoms.set_constraint(FixAtoms(indices=args.indices))

    if args.output:
        write(args.output, atoms, vasp5=True, sort=args.sort)

    else:
        print(atoms)

    return None
