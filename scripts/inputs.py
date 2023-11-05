#!/bin/env python3

import argparse
from ase.calculators.vasp import Vasp
from ase.io import read, write

from pymatgen.io.vasp.inputs import Potcar, Kpoints, Incar
from pymatgen.symmetry.kpath import KPathSeek

def get_atoms(args):
    '''Creates ASE atoms object from a file'''

    atoms = read(args.file)
    
    return atoms

def write_potcar(args):
    '''Writes a POTCAR file'''
    
    atoms = args.atoms
    #get symbols
    symbols = atoms.get_chemical_symbols()

    potcar = Potcar(symbols, functional='PBE')
    potcar.write_file(f'{args.directory}/POTCAR')

    return None

def write_kpoints(args):
    '''Writes a KPOINTS file'''

    kpoints = Kpoints.gamma_automatic(kpts=args.kpoints)
    kpoints.write_file(f'{args.directory}/KPOINTS')

    return None

def write_kpath(args):
    '''Writes a KPOINTS file for band structure calculation'''

    kpath = KPathSeek(structure=args.atoms, symprec=args.symprec)




def setup_args(subparsers):
    subp_inputs = subparsers.add_parser("inputs", help="Generate VASP inputs")

    subp_inputs.add_argument("-f", "--file", type=argparse.FileType('r'), default="POSCAR", help="Input file")
    subp_inputs.add_argument("-d", "--directory", type=str, default=".", help="Directory to write VASP inputs to")
    subp_inputs.add_argument("-p", "--potcar", type=bool, default=False, help="Write POTCAR file")
    subp_inputs.add_argument("-k", "--kpoints", type=int, nargs=3, default=None, help="Writes gamma centered KPOINTS file")
    # subp_inputs.add_argument("-i", "--incar", type=str, default=None, help="INCAR file type")
    subp_inputs.add_argument("--kpath", type=int, default=20, help="KPOINTS file for band structure calculation")
    subp_inputs.add_argument("--symprec", type=float, default=0.01, help="Symmetry precision for SeekPath algorithm")

def run(args):

    if args.potcar:
        write_potcar(args)

    if args.kpoints:
        write_kpoints(args)

    if args.kpath:
        write_kpath(args)

    return None


