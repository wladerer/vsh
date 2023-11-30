#!/usr/bin/env python3

from jinja2 import Template

import os
import json

from ase.io import read

from mp_api.client import MPRester
from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Potcar, Kpoints, Poscar, Incar
from pymatgen.symmetry.bandstructure import HighSymmKpath

two_d_kpath_template = """
Two dimensional Kpath 
   {{kpath}}
Line-Mode
Reciprocal
   0.5000000000   0.0000000000   0.0000000000     M
   0.3333333333   0.3333333333   0.0000000000     K

   0.3333333333   0.3333333333   0.0000000000     K
   0.0000000000   0.0000000000   0.0000000000     GAMMA

   0.0000000000   0.0000000000   0.0000000000     GAMMA
   0.5000000000   0.0000000000   0.0000000000     M

"""


def get_atoms(args):
    '''Creates ASE atoms object from a file'''

    atoms = read(args.input)
    
    return atoms

def write_potcar(args):
    '''Writes a POTCAR file'''
    
    structure = args.input
    #get symbols
    symbols = structure.get_chemical_symbols()

    potcar = Potcar(symbols, functional='PBE_54')

    if not args.output:
        print(potcar)

    else:
        potcar.write_file(f'{args.output}')

    return potcar

def write_kpoints(args):
    '''Writes a KPOINTS file'''

    kpoints = Kpoints.gamma_automatic(kpts=args.kpoints)

    if not args.output:
        print(kpoints)

    else:
        kpoints.write_file(f'{args.output}')

    return kpoints


def write_kpath(args) -> Kpoints:
    '''
    Makes a linemode Kpoints object from a structure
    '''
    structure = Structure.from_file(args.input)
    kpath = HighSymmKpath(structure)
    kpoints = Kpoints.automatic_linemode(args.kpath, kpath)
    
    if not args.output:
        print(kpoints)
    else:
        kpoints.write_file(f'{args.output}')

    return kpoints

def write_kplane(args) -> str:
    '''Creates a 2D kpath from a jinja 2 template'''
    
    template = Template(two_d_kpath_template)
    kplane = template.render(kpath=args.kplane)
    
    if not args.output:
        print(kplane)
    else:
        with open(args.output, "w") as f:
            f.write(kplane)
            
    return kplane
    

def sort_poscar(args) -> Poscar:
    structure = Structure.from_file(args.input)
    poscar = Poscar(structure, sort_structure=True)
    
    if not args.output:
        print(poscar.get_str())
    else:
        poscar.write_file(f'{args.output}')

    return poscar


def structure_from_mpi_code(mpcode: str, api_key: str, is_conventional: bool = True) -> Structure:
    '''
    Creates a pymatgen structure from a code
    '''
    if not mpcode.startswith("mp-"):
        mpcode = "mp-"+mpcode

    with MPRester(api_key) as mpr:
        structure = mpr.get_structure_by_material_id(
            mpcode, conventional_unit_cell=is_conventional)

    return structure


def mp_poscar(args):
    '''Creates a POSCAR file from a Materials Project code'''
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


def write_incar(args) -> dict:
    '''Loads a dictionary from the incar.json file'''
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

def run(args):
    functions = {
        "potcar": write_potcar,
        "kpoints": write_kpoints,
        "kpath": write_kpath,
        "kplane": write_kplane,
        "sort": sort_poscar,
        "mp_poscar": mp_poscar,
        "incar": write_incar,
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)

    return None


