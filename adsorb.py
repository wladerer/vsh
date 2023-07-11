import argparse
from ase.io import read, write
from ase import Atoms
import numpy as np


def adsorbate_from_file(infile: str) -> Atoms:
    '''Reads an adsorbate from a file'''
    adsorbate = read(infile)
    return adsorbate

def set_pbc(atoms: Atoms, pbc: tuple[bool]) -> Atoms:
    '''Sets the pbc of an atoms object'''
    atoms.set_pbc(pbc)
    return atoms

def get_topmost_atom(atoms: Atoms) -> float:
    '''Gets the height of the slab'''
    return np.max(atoms.positions[:,2])

def add_adsorbate_by_coordinate(atoms: Atoms, adsorbate: Atoms | str, coords: list[float]) -> Atoms:
        '''Adds an adsorbate above a surface using user defined coordinates'''
        print(coords)
        atoms.extend(Atoms(adsorbate))
        
        return atoms

def add_adsorbate_by_index(atoms: Atoms, adsorbate: Atoms | str, index: int) -> Atoms:
    '''Adds an adsorbate above a surface using the index of the topmost atom'''
    z = get_topmost_atom(atoms)
    atoms.extend(Atoms(adsorbate, positions=[atoms[index].position[0], atoms[index].position[1], z]))
    
    return atoms


def write_adsorbed_slab(atoms: Atoms, outfile: str, sort: bool = True):
    '''Writes adsorbed slab to file'''
    write(outfile, atoms, format='vasp', sort=sort)
    
    return None

def get_surface_atoms(atoms: Atoms, tolerance: float = 0.01) -> dict:
    '''Returns a list of surface atoms and their indices. Only works for flat surfaces'''
    surface_indices = []
    z = get_topmost_atom(atoms)
    for atom in atoms:
        if atom.position[2] > z - tolerance:
            surface_indices.append(atom.index)

    surface_atom_types = []
    surface_atom_coordinates = []
    for atom in surface_indices:
        surface_atom_types.append(atoms[atom].symbol)
        surface_atom_coordinates.append(atoms[atom].position)

    surface_atoms: dict = {'indices': surface_indices, 'types': surface_atom_types, 'coordinates': surface_atom_coordinates}

    return surface_atoms

def print_surface_atoms(surface_atoms_dictionary: dict):
    '''Prints the surface atoms'''
    #format it nicely
    #Type Index Coordinates
    for atom in surface_atoms_dictionary['indices']:
        print(f"{surface_atoms_dictionary['types'][atom]} {atom} {surface_atoms_dictionary['coordinates'][atom]}")

    return None 


def adsorbate_utilities():
    parser = argparse.ArgumentParser(description='A utility for adsorbing molecules on surfaces')

    #structure file -f or --file
    parser.add_argument('-f', '--file', type=str, help='The structure file to be adsorbed', required=True)
    parser.add_argument('-a', '--adsorbate', type=str, help='The adsorbate to be adsorbed in string format', required=False)
    parser.add_argument('-A', '--adsorbate-file', type=str, help='Allows the user to specify a file containing the adsorbate to be adsorbed')
    parser.add_argument('-c', '--coordinates', type=float, nargs=3, help='The coordinates of the adsorbate', required=False)
    #adsorbate index -i or --index
    parser.add_argument('-I', '--index', type=int, help='The index of a target atom', required=False)
    #output file -o or --output, default is to print to the contents of the file to stdout
    parser.add_argument('-o', '--output', type=str, help='Name of the output file', required=False)
    parser.add_argument('--pbc', type=bool, nargs=3, help='Sets the pbc of the structure file', required=False, default=[True, True, False])
    parser.add_argument('--surface', action='store_true', help='Prints the surface atoms of the structure file', required=False)
    args = parser.parse_args()

    #read in the structure file
    atoms = read(args.file)

    if args.surface:
        surface_atoms = get_surface_atoms(atoms)
        print_surface_atoms(surface_atoms)
        #exit the program
        exit()

    atoms = set_pbc(atoms, args.pbc)

    #read in the adsorbate and 
    if args.adsorbate:
        adsorbate: str = args.adsorbate

    elif args.adsorbate_file:
        adsorbate: Atoms = read(args.adsorbate_file)

    
    if args.coordinates:
        atoms = add_adsorbate_by_coordinate(atoms, adsorbate, args.coordinates)
    
    if args.index:
        #get the coordinates of the surface atom index
        coordinates = atoms[args.index].position
        #add an offset to the z coordinate of 2.0
        coordinates[2] += 2.0
        atoms = add_adsorbate_by_coordinate(atoms, adsorbate, coordinates)


    # #write the adsorbed slab to file
    # if args.output == 'stdout':
    #     atom_types = [ atom.symbol for atom in atoms ]
    #     atom_coordinates = [ atom.position for atom in atoms ]
    #     for atom in range(len(atom_types)):
    #         print(f"{atom_types[atom]} {atom_coordinates[atom]}")
    
    if args.output:
        write_adsorbed_slab(atoms, args.output)

    return None

if __name__ == '__main__':
    adsorbate_utilities()