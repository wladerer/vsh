#!/usr/bin/env python3

import argparse
import os
import json

from ase.io import read

from mp_api.client import MPRester
from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Potcar, Kpoints, Poscar, Incar
from pymatgen.symmetry.kpath import KPathSeek

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
    potcar.write_file(f'{args.directory}/potcar.vsh')

    return None

def write_kpoints(args):
    '''Writes a KPOINTS file'''

    kpoints = Kpoints.gamma_automatic(kpts=args.kpoints)
    kpoints.write_file(f'{args.directory}/kpoints.vsh')

    return None

def write_kpath(args):
    '''Writes a KPOINTS file for band structure calculation'''

    kpath = KPathSeek(structure=args.atoms, symprec=args.symprec)
    kpoints = kpath.kpath['kpoints']
    kpoints.write_file(f'{args.directory}/kpath.vsh')
    

def sort_poscar(poscar_file: str) -> Poscar:
    structure = Poscar.from_file(poscar_file).structure
    poscar = Poscar(structure, sort_structure=True)
    poscar.write_file(poscar_file)


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


def to_poscar(structure: Structure, filename: str = "POSCAR") -> None:
    '''
    Creates a POSCAR file from a pymatgen structure
    '''
    poscar = Poscar(structure, sort_structure=True)
    poscar.write_file(filename)

def mp_poscar(mp_code: str):
    '''Creates a POSCAR file from a Materials Project code'''
    #check if the MP_API_KEY is set in the environment
    if "MP_API_KEY" not in os.environ:
        raise ValueError("MP_API_KEY not set in environment variables")
        
    api_key = os.environ["MP_API_KEY"]
    structure = structure_from_mpi_code(mp_code, api_key, is_conventional=True)
    to_poscar(structure)

    return None   

def mp_primitive(mp_code: str):
    '''Creates a primtive POSCAR file from a Materials Project code'''
    #check if the MP_API_KEY is set in the environment
    if "MP_API_KEY" not in os.environ:
        raise ValueError("MP_API_KEY not set in environment variables")
    
    api_key = os.environ["MP_API_KEY"]
    structure = structure_from_mpi_code(mp_code, api_key, is_conventional=False)
    to_poscar(structure)

def write_incar(dict_key: str) -> dict:
    '''Loads a dictionary from the incar.json file'''
    script_dir = os.path.dirname(__file__)
    docs_dir = os.path.join(script_dir, '..', 'docs')
    file_path = os.path.join(docs_dir, 'incars.json')

    with open(file_path, "r") as f:
        incar_dict = json.load(f)

    incar = Incar.from_dict(incar_dict[dict_key])
    incar.write_file("./INCAR")

# def summarize(directory: str = './'):
#     '''Summarizes the INCAR, POSCAR, and KPOINTS files in the directory'''

#     #check if the directory exists
#     if not os.path.isdir(directory):
#         raise ValueError(f"{directory} does not exist")
    
#     #check if the INCAR, POSCAR, and KPOINTS files exist

#     for file in ["INCAR", "POSCAR", "KPOINTS"]:
#         if not os.path.isfile(f"{directory}/{file}"):
#             raise ValueError(f"{directory}/{file} does not exist")
        
#     #load the input files
#     incar = Incar.from_file(f"{directory}/INCAR")
#     kpoints = Kpoints.from_file(f"{directory}/KPOINTS")
#     poscar = Poscar.from_file(f"{directory}/POSCAR")

#     #get the unit cell parameters and symmetry group from the POSCAR
#     unit_cell = poscar.structure.lattice
#     symmetry = poscar.structure.get_space_group_info()

#     #get kpoints type
#     kpoints_type = kpoints.style

#     #get the INCAR parameters
#     incar_dict = incar.as_dict()

    

def setup_args(subparsers):
    subp_inputs = subparsers.add_parser("inputs", help="Generate VASP inputs")

    subp_inputs.add_argument("-f", "--file", type=str, default=None, help="Input file")
    subp_inputs.add_argument("-d", "--directory", type=str, default=".", help="Directory to write VASP inputs to")
    subp_inputs.add_argument("--potcar", type=bool, default=False, help="Write POTCAR file")
    subp_inputs.add_argument("-k", "--kpoints", type=int, nargs=3, default=None, help="Writes gamma centered KPOINTS file")
    subp_inputs.add_argument("-i", "--incar", type=str, default=None, help="INCAR file type", choices=["bulk", "slab", "band", "single-point", "band-soc", "band-slab-soc"])
    subp_inputs.add_argument("--kpath", type=int, default=None, help="KPOINTS file for band structure calculation")
    subp_inputs.add_argument("--symprec", type=float, default=0.01, help="Symmetry precision for SeekPath algorithm")
    subp_inputs.add_argument("--sort", action="store_true", help="Sort atoms in POSCAR file")
    subp_inputs.add_argument("--freeze", type=str, default=None, help="Freeze atoms in POSCAR file")
    subp_inputs.add_argument("--mp-poscar", type=str, default=None, help="Get POSCAR file from Materials Project")
    subp_inputs.add_argument("--mp-primitive", type=str, default=None, help="Get primitive POSCAR file from Materials Project")

def run(args):

    if args.potcar:
        write_potcar(args)

    if args.kpoints:
        write_kpoints(args)

    if args.kpath:
        write_kpath(args)

    if args.sort:
        sort_poscar(args.file)

    if args.mp_poscar:
        mp_poscar(args.mp_poscar)

    if args.mp_primitive:
        mp_primitive(args.mp_primitive)

    if args.incar:
        write_incar(args.incar)


    return None


