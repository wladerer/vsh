#!/bin/env python3

import argparse
from ase.io import read
import os
from pymatgen.io.vasp.outputs import Vasprun
from ase.db import connect


def check_for_vasprun(file: str) -> bool:
    """Checks if a vasprun.xml file exists and is valid"""
    is_file = os.path.isfile(file)

    if is_file:
        try:
            vasprun_object = Vasprun(file)
        except:
            raise ValueError("vasprun.xml file is invalid. Calculation may be running or corrupt")

    else:
        raise ValueError(f"{file} not found")
    
def handle_kpoints(kpoints: list[tuple]) -> str:
    """Handles kpoints returned by pymatgen"""
    if len(kpoints) == 1:
        #this is an automatic generated mesh, just return the value as a string
        return str(kpoints[0])
    else:
        #this is a manual mesh, return the values as a string
        return str(kpoints)



def get_metadata(file: str) -> dict:
    """Returns metadata from vasprun.xml file"""
    #check for vasprun.xml file
    check_for_vasprun(file)
    vasprun = Vasprun(file)
    
    spin = vasprun.parameters['ISPIN']
    soc = vasprun.parameters['LSORBIT']
    xc = vasprun.parameters['GGA']
    kpoints = handle_kpoints(vasprun.kpts)
    converged_ionic = vasprun.converged_ionic
    converged_electronic = vasprun.converged_electronic

    metadata = {'spin': spin, 'soc': soc, 'xc': xc, 'kpoints': kpoints, 'ionic': converged_ionic, 'electronic': converged_electronic}


    return metadata

def check_for_vasprun(file: str) -> bool:
    """Checks if a vasprun.xml file exists"""
    if os.path.isfile(file):
        return True
    else:
        return False
    

def update_ase_db(vasprun_file: str, database: str):
    '''Writes atoms and metadata to a database'''
    atoms = read(vasprun_file)
    metadata = get_metadata(vasprun_file)
    db = connect(database)
    db.write(atoms, xc=metadata['xc'], spin=metadata['spin'], soc=metadata['soc'], kpoints=metadata['kpoints'], ionic=metadata['ionic'], electronic=metadata['electronic'])
    
    return None

def parse_args():
    '''Parse command line arguments'''
    parser = argparse.ArgumentParser(description='Reads VASP output files and writes to a database')
    parser.add_argument('-f', '--file', default='vasprun.xml', type=str, help='vasprun.xml file', required=True)
    parser.add_argument('-d', '--database', type=str, help='Database file', required=True)

    args = parser.parse_args()

    return args



if __name__ == "__main__":
    args = parse_args()
    update_ase_db(args.file, args.database)