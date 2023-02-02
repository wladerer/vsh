# vsh
Command line utilities for interacting with VASP

## Functions

- `getNbands` - Get the number of bands from an OUTCAR file
- `getNatoms` - Get the number of atoms from an OUTCAR file
- `getEfermi` - Get the Fermi energy from an OUTCAR file
- `getElements` - Get the element list from a POSCAR file
- `updateTag` - Update a tag in an INCAR file
- `isConverged` - Check if a VASP job has converged (optional flag to check all subdirectories in the current directory)
- `restartVasp` - Restart VASP jobs that have not converged

## Usage

The functions can be used by sourcing the file in your shell. 

## Configuration

A configure.sh script has been provided to update your ~/.bashrc so that it knows to source both the v.sh (where all functions are stored)
and the vsh/.vshrc file where specific environment variables are set (e.g path to potential files, default incars, and other important defaults).



