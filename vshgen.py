#!/bin/env python3

import argparse
from ase.calculators.vasp import Vasp
from ase.io import read, write

from pymatgen.io.vasp.inputs import Potcar, Kpoints, Incar

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

# def write_kpoints(args):
#     '''Writes a KPOINTS file'''

#     atoms = args.atoms



def parse_args():
    parser = argparse.ArgumentParser(description="Create VASP inputs using ASE")

    parser.add_argument("-f", "--file", type=argparse.FileType('r'), default="POSCAR", help="Input file")
    parser.add_argument("-d", "--directory", type=str, default=".", help="Directory to write VASP inputs to")
    parser.add_argument("-p", "--potcar", type=bool, default=False, help="Write POTCAR file")
    parser.add_argument("-k", "--kpoints", type=int, nargs=3, default=None, help="Writes gamma centered KPOINTS file")
    parser.add_argument("-i", "--incar", type=str, default=None, help="INCAR file type")

    args = parser.parse_args()


    args.atoms = get_atoms(args)
    
    return args


def main():
    args = parse_args()
    


if __name__ == "__main__":
    main()
