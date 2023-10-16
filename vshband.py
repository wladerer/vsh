#!/bin/env python3

import argparse
from ase.calculators.vasp import Vasp
from ase.io import read, write
import os
import pyprocar

orbital_dict = {'s': 0, 'p_y': 1, 'p_z': 2, 'p_x': 3, 'd_xy': 4, 'd_yz': 5, 'd_z2': 6, 'd_xz': 7, 'd_x2-y2': 8}

def handle_orbitals(orbitals: list | str) -> list[int]:
    '''Converts a string to a list of orbitals'''

    if 'all' in orbitals:
        orbital_list = list(range(9))

    elif 's' in orbitals:
        orbital_list = [0]
    
    elif 'p' in orbitals:
        orbital_list = [1, 2, 3]
    
    elif 'd' in orbitals:
        orbital_list = [4, 5, 6, 7, 8]

    #if orbitals is a string, convert to indices
    elif isinstance(args.orbitals, str):
        orbital_list = [orbital_dict[args.orbitals]]

    #if orbitals is a list of strings, convert to indices
    elif isinstance(args.orbitals, list):
        orbital_list = [orbital_dict[orbital] for orbital in args.orbitals]

    return orbital_list


def handle_atoms(poscar: str = './POSCAR') -> dict:
    '''Gets identities and indices of atoms from a POSCAR or CONTCAR file'''

    atoms = read(poscar)
    
    #get list of atom types
    atom_types = atoms.get_chemical_symbols()

    #get dictionary of atom types and indices
    atom_indices = {}
    for i, atom in enumerate(atom_types):
        if atom not in atom_indices:
            atom_indices[atom] = []
        atom_indices[atom].append(i)

    return atom_indices

def plot():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e','--elimit', type=float, nargs='+', default=[-2,2], help='Range of energy to plot')
    parser.add_argument('-m', '--mode', type=str, default='parametric', help='Plotting mode')
    parser.add_argument('--orbitals', type=int, nargs='+', default=None, help='Orbitals to plot')
    parser.add_argument('--spins', type=int, nargs='+', default=None, help='Spins to plot')
    parser.add_argument('--atoms', type=int, nargs='+', default=None, help='Atoms to plot')
    parser.add_argument('--cmap', type=str, default='cool', help='Color map')
    parser.add_argument('--clim', type=float, nargs='+', default=[0,1], help='Color map limits')
    parser.add_argument('--code', type=str, default='vasp', help='Code used to generate the data')
    parser.add_argument('--dirname', type=str, default='.', help='Directory where the data is stored')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file name')
    parser.add_argument('--fermi', type=float, default=None, help='Fermi energy (eV)')
    parser.add_argument('--dpi', type=int, default=600, help='DPI of the output file')

    args = parser.parse_args()

    #if atoms is a string, use handle atoms to convert to indices
    if args.atoms:

        if isinstance(args.atoms, str):
            atom_dict = handle_atoms(args.atoms)
            args.atoms = atom_dict[args.atoms]
            


    if args.output:
        plot = pyprocar.bandsplot(code=args.code,
                           mode=args.mode,
                           dirname=args.dirname,
                           orbitals=args.orbitals,
                           spins=args.spins,
                           cmap=args.cmap,
                           clim=args.clim,
                           elimit=args.elimit,
                           fermi=args.fermi,
                           show=False)

        plot.fig.savefig(args.output, dpi=args.dpi)

    else:
        pyprocar.bandsplot(code=args.code,
                           mode=args.mode,
                           dirname=args.dirname,
                           orbitals=args.orbitals,
                           spins=args.spins,
                           cmap=args.cmap,
                           clim=args.clim,
                           elimit=args.elimit,
                           fermi=args.fermi
                           )

# if __name__ == '__main__':
#     plot()

atoms = handle_atoms('/Users/wladerer/github/vsh/test/files/snpt3.vasp')
print(atoms)