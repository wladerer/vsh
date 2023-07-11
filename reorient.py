#!/usr/bin/env python
from pymatgen.core.structure import Structure, Molecule
import argparse

M = [[0,0,-1],[0,-1,0],[-1,0,0]]

def read_file(filename):
    '''Reads a molecule from a file.'''
    return Molecule.from_file(filename)

def reorient(molecule, M):
    '''Reorients a molecule using a transformation matrix, M.'''
    new_coords = molecule.cart_coords.dot(M)
    return Molecule(molecule.species, new_coords)

def save_file(molecule, filename):
    '''Saves a molecule to a file.'''
    molecule.to(filename=filename)

def parse_args():
    '''Parses command line arguments.'''
    parser = argparse.ArgumentParser(description='Reorients a molecule.')
    #arguments: -f filename, -o output filename (default is original file + _reoriented.xyz), -m transformation matrix (default: M)
    parser.add_argument('-f', '--filename', help='The filename of the molecule to be reoriented.', required=True)
    parser.add_argument('-o', '--output', help='The filename of the reoriented molecule.', required=False)
    parser.add_argument('-m', '--matrix', help='The transformation matrix to be used for reorienting the molecule.', required=False)
    args = parser.parse_args()

    return args

def reorient_molecule(molecule, M):
    args = parse_args()

    #read in the molecule
    molecule = read_file(args.filename)

    #reorient the molecule
    molecule = reorient_molecule(molecule, M)

    #save the molecule
    if args.output:
        save_file(molecule, args.output)
    else:
        save_file(molecule, args.filename[:-4]+'_reoriented.xyz')



