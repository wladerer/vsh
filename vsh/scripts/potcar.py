from ase.io import read, write

def get_atoms(args):
    '''Creates ASE atoms object from a file'''

    atoms = read(args.input)
    
    return atoms

def write_potcar(args):
    '''Writes a POTCAR file'''
    from pymatgen.io.vasp.inputs import PotcarSingle, Poscar, Potcar
    # Load POSCAR file
    poscar = Poscar.from_file(args.input)

    # Extract unique elements from the POSCAR
    unique_elements = poscar.site_symbols


    # Create a POTCAR file
    potcar = Potcar(symbols=unique_elements)

    if not args.output:
        print(potcar.__str__())

    else:
        potcar.write_file(f'{args.output}')

    return potcar

