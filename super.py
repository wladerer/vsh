import argparse
from ase.io import read, write
from ase.build.supercells import make_supercell

def create_super_cell():
    parser = argparse.ArgumentParser(description='Create supercell using ASE')

    parser.add_argument('-f', '--file', type=str, help='Structure file')
    parser.add_argument('-s', '--supercell', type=int, nargs=3, default=[1, 1, 1], help='Supercell size along each lattice vector')
    parser.add_argument('-o', '--output', type=str, default='super.vasp' , help='Output file name')
    #sort atoms
    parser.add_argument('--sort', action='store_true', help='Sort atoms')
    #add vacuum
    parser.add_argument('--vacuum', type=float, default=0.0, help='Vacuum size')

    args = parser.parse_args()
    atoms = read(args.file)
    x_rep, y_rep, z_rep = args.supercell
    M = [[x_rep, 0, 0], [0, y_rep, 0], [0, 0, z_rep]]
    supercell = make_supercell(atoms, M)

    if args.vacuum > 0.0:
        supercell.center(vacuum=args.vacuum, axis=2)

    write(args.output, supercell, vasp5=True, sort=args.sort)


if __name__ == '__main__':
    create_super_cell()


    
    
