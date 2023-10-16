import argparse
from ase.calculators.vasp import Vasp
from ase.io import read, write
import os
import pyprocar

def handle_atoms(poscar: str) -> dict:
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