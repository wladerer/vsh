from ase.io import read
import os
import json

def get_atoms(args):
    '''Creates ASE atoms object from a file'''

    atoms = read(args.input)
    
    return atoms

def write_incar(args) -> dict:
    '''Loads a dictionary from the incar.json file'''
    from pymatgen.io.vasp.inputs import Incar
    
    script_dir = os.path.dirname(__file__)
    docs_dir = os.path.join(script_dir, '../..', 'docs') #watch
    file_path = os.path.join(docs_dir, 'incars.json')

    with open(file_path, "r") as f:
        incar_dict = json.load(f)

    incar = Incar.from_dict(incar_dict[args.incar])

    if not args.output:
        print(incar.get_str())
    else:
        incar.write_file(f'{args.output}')
        
    return None

def update_incar_tag(args) -> None:
    '''Updates tags in an INCAR file'''
    from pymatgen.io.vasp.inputs import Incar
    
    incar = Incar.from_file(args.input)
    
    incar[args.update[0]] = args.update[1]

    if not args.output:
        print(incar.get_str())
    else:
        incar.write_file(f'{args.output}')
        
    return None

