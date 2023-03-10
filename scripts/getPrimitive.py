#python script to get the POSCAR file from materials project

import sys
import os
from mp_api.client import MPRester
from pymatgen.core import Structure
from pymatgen.io.vasp import Poscar

def structure_from_mpi_code(mpcode: str, api_key: str, is_conventional: bool = False) -> Structure:
    '''
    Creates a pymatgen structure from a code
    '''
    if not mpcode.startswith("mp-"):
        mpcode = "mp-"+mpcode

    with MPRester(api_key) as mpr:
        structure = mpr.get_structure_by_material_id(mpcode, conventional_unit_cell=is_conventional)

    return structure

def to_poscar(structure: Structure, filename: str = "POSCAR") -> None:
    '''
    Creates a POSCAR file from a pymatgen structure
    '''
    poscar = Poscar(structure, sort_structure=True)
    poscar.write_file(filename)

if __name__ == "__main__":

    api_key = os.environ.get("MP_API_KEY")
    #remove quotes from api_key 
    api_key = api_key.replace('"', '')


    if api_key is None:
        raise ValueError("No API key found. Please set the MP_API_KEY environment variable.")
    
    mpcode = sys.argv[1] 
    structure = structure_from_mpi_code(mpcode, api_key)
    to_poscar(structure)
