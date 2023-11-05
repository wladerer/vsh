#!/usr/bin/env python3

from ase.io import read, write
import pyprocar

orbital_dict = {'s': 0, 'p_y': 1, 'p_z': 2, 'p_x': 3, 'd_xy': 4, 'd_yz': 5, 'd_z2': 6, 'd_xz': 7, 'd_x2-y2': 8, 'f_y(3x2 -y2)': 9, 'f_xyz': 10, 'f_yz2':11, 'f_z3':12, 'f_xz2':13, 'f_z(x2 -y2)':14, 'f_x(x2 -3y2)':15}

def handle_orbitals(orbitals: list | str) -> list[int]:
    '''Converts a string to a list of orbitals'''

    if 'all' in orbitals:
        orbital_list = list(range(16))

    elif 's' in orbitals:
        orbital_list = [0]
    
    elif 'p' in orbitals:
        orbital_list = [1, 2, 3]
    
    elif 'd' in orbitals:
        orbital_list = [4, 5, 6, 7, 8]
    
    elif 'f' in orbitals:
        orbital_list = [9, 10, 11, 12, 13, 14, 15]

    #if orbitals is a string, convert to indices
    elif isinstance(orbitals, str):
        orbital_list = [orbital_dict[orbitals]]

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

def setup_args(subparsers):
    subp_band = subparsers.add_parser('bands', help='Plot band structure')

    subp_band.add_argument('-e','--elimit', type=float, nargs='+', default=[-2,2], help='Range of energy to plot')
    subp_band.add_argument('-m', '--mode', type=str, default='parametric', help='Plotting mode')
    subp_band.add_argument('--orbitals', nargs='+', default=None, help='Orbitals to plot')
    subp_band.add_argument('--spins', type=int, nargs='+', default=None, help='Spins to plot')
    subp_band.add_argument('--atoms', type=int, nargs='+', default=None, help='Atoms to plot')
    subp_band.add_argument('--cmap', type=str, default='cool', help='Color map')
    subp_band.add_argument('--clim', type=float, nargs='+', default=[0,1], help='Color map limits')
    subp_band.add_argument('--code', type=str, default='vasp', help='Code used to generate the data')
    subp_band.add_argument('--dirname', type=str, default='.', help='Directory where the data is stored')
    subp_band.add_argument('-o', '--output', type=str, default=None, help='Output file name')
    subp_band.add_argument('--fermi', type=float, default=None, help='Fermi energy (eV)')
    subp_band.add_argument('--dpi', type=int, default=800, help='DPI of the output file')


def run(args):

    args.orbitals = handle_orbitals(args.orbitals)


    plot = pyprocar.bandsplot(code=args.code,
                           mode=args.mode,
                           dirname=args.dirname,
                           orbitals=args.orbitals,
                           atoms=args.atoms,
                           spins=args.spins,
                           cmap=args.cmap,
                           clim=args.clim,
                           elimit=args.elimit,
                           fermi=args.fermi,
                           show=args.output is None)

    if args.output:
        plot.fig.savefig(args.output, dpi=args.dpi)

