from ase.io import read, write
import os

def get_atoms(args):
    '''Creates ASE atoms object from a file'''

    atoms = read(args.input)
    
    return atoms

def sort_poscar(args):
    '''Sorts a POSCAR file'''
    from pymatgen.core import Structure
    from pymatgen.io.vasp.inputs import Poscar

    structure = Structure.from_file(args.input)
    poscar = Poscar(structure, sort_structure=True)
    
    if not args.output:
        print(poscar.get_str())
    else:
        poscar.write_file(f'{args.output}')

    return poscar


def structure_from_mpi_code(mpcode: str, api_key: str, is_conventional: bool = True):
    '''
    Creates a pymatgen structure from a code
    '''
    from mp_api.client import MPRester
    if not mpcode.startswith("mp-"):
        mpcode = "mp-"+mpcode

    with MPRester(api_key) as mpr:
        structure = mpr.get_structure_by_material_id(
            mpcode, conventional_unit_cell=is_conventional)

    return structure


def mp_poscar(args):
    '''Creates a POSCAR file from a Materials Project code'''
    from pymatgen.io.vasp.inputs import Poscar 

    #check if the MP_API_KEY is set in the environment
    if "MP_API_KEY" not in os.environ:
        raise ValueError("MP_API_KEY not set in environment variables")
        
    api_key = os.environ["MP_API_KEY"]
    structure = structure_from_mpi_code(args.mp_poscar, api_key, is_conventional=( not args.primitive) )

    poscar = Poscar(structure, sort_structure=args.sort)

    if not args.output:
        print(poscar.get_str())    
    else:
        poscar.write_file(f'{args.output}')

    return poscar

def convert_to_poscar(args):
    '''Converts a file to a POSCAR file'''
    from pymatgen.io.vasp.inputs import Poscar 

    structure = read(args.input)
    poscar = Poscar(structure, sort_structure=args.sort)

    if not args.output:
        print(poscar.get_str())    
    else:
        poscar.write_file(f'{args.output}')

    return poscar

def make_supercell(args):
    '''Make a supercell of a structure'''
    from pymatgen.io.vasp.inputs import Poscar
    from pymatgen.core import Structure
    from pymatgen.transformations.standard_transformations import SupercellTransformation
    
    structure = Structure.from_file(args.input)
    transformation = SupercellTransformation(args.super)
    supercell = transformation.apply_transformation(structure)
    
    poscar = Poscar(supercell, sort_structure=args.sort)
    
    if not args.output:
        print(poscar.get_str())
    else:
        poscar.write_file(f'{args.output}')
    

def run(args):
    functions = {
        "sort": sort_poscar,
        "mp_poscar": mp_poscar,
        "convert": convert_to_poscar,
        "super": make_supercell
    }
    
    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)