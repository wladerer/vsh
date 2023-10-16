#!/bin/env python3

import argparse
from ase.calculators.vasp import Vasp
from ase.io import read, write


def parse_args():
    parser = argparse.ArgumentParser(description="Create VASP inputs using ASE")
    # Structure parameters from file -f or --file
    def poscar_file(x):
        with open(x, 'r') as f:
            return read(f)
    parser.add_argument("atoms", 
                        type=poscar_file, 
                        metavar='poscar',
                        help="Structure file")
    # Electronic parameters
    parser.add_argument("--encut", 
                        type=float, 
                        help="Cutoff energy for plane waves")
    parser.add_argument("--ediff", 
                        type=float, 
                        help="Energy convergence criterion")
    parser.add_argument("--ediffg", 
                        type=float, 
                        help="Force convergence criterion")
    parser.add_argument("--algo",
                        type=str,
                        choices=["Normal", "Fast", "VeryFast"],
                        help="Electronic minimization algorithm")
    parser.add_argument("--isif",
                        type=int,
                        choices=[0, 1, 2, 3, 4, 5, 6, 7],
                        help="Ionic relaxation method")
    # Add more arguments as needed
    parser.add_argument("--nsw", 
                        type=int, 
                        help="Number of ionic steps")
    parser.add_argument("--ibrion", 
                        type=int, 
                        help="Ionic relaxation algorithm")
    parser.add_argument("--potim", 
                        type=float, 
                        help="Ionic relaxation time step")
    parser.add_argument("--nelm", 
                        type=int, 
                        help="Number of electronic steps")
    parser.add_argument("--ispin", 
                        type=int, 
                        help="Spin polarization")
    # Kpoints parameters
    parser.add_argument("--kpts",
                        type=int,
                        nargs=3,
                        default=[1, 1, 1],
                        help="Number of kpoints along each reciprocal lattice vector")
    parser.add_argument("--kgamma", 
                        action="store_true", 
                        help="Use Gamma-centered kpoint grid")
    #FIXME IMPLEMENT THIS PARAMETER
    #parser.add_argument("--linemode", 
    #                    action="store_true", 
    #                    help="Use line mode for band structure")
    parser.add_argument("--xc", # exchange correlation
                        type=str, 
                        default="pbe", 
                        help="Exchange-correlation functional")
    parser.add_argument("--npar", # parallelization
                        type=int, 
                        help="Number of cores to use")
    # IO parameters
    parser.add_argument("--lwave", 
                        action="store_true", 
                        help="Write WAVECAR")
    parser.add_argument("--lcharg", 
                        action="store_true", 
                        help="Write CHGCAR")
    parser.add_argument("--lreal",
                        type=str,
                        choices=["Auto", "None", "A", "B", "C"],
                        help="Type of real-space projection")
    parser.add_argument("--laechg", 
                        action="store_true", 
                        help="Write AECCAR0 and AECCAR2")
    parser.add_argument("--prec", # Precision
                        type=str, 
                        choices=["N", "L", "M", "H", "A"], 
                        help="Precision")
    # Symmetry parameters
    parser.add_argument("--symprec", 
                        type=float, 
                        help="Symmetry precision")
    parser.add_argument("--isym", 
                        type=int, 
                        choices=[-1, 0, 1, 2, 3])
    parser.add_argument("--icharg", # Charge density
                        type=int,
                        choices=[0, 1, 2, 4, 10, 11, 12],
                        help="Charge density initialization")
    parser.add_argument("--lsorbit", # Spin-Orbit coupling
                        action="store_true", 
                        help="Spin orbit coupling")
    # Smearing parameters
    parser.add_argument("--ismear",
                        type=int, 
                        choices=[-5, -4, -3, -2, -1, 0, 1], 
                        help="Smearing method")
    parser.add_argument("--sigma", 
                        type=float, 
                        help="Smearing width")
    parser.add_argument("--magmom", 
                        type=eval, 
                        help="PYTHON list of integers of magnetic moments\
                        in the order they appear in the file")
    args = parser.parse_args()
    # Process arguments
    natoms = args.atoms.get_global_number_of_atoms()
    if len(args.magmom) != natoms:
        raise Exception('Length of the MAGMOM list should be == number of atoms')
    return args


def create_vasp_inputs(args):
    # Use the specified arguments to create the Vasp calculator
    calc = Vasp(**vars(args))
    atoms.calc = calc
    calc.write_input(atoms)


def main():
    args = parse_args()
    create_vasp_inputs(args)


if __name__ == "__main__":
    main()
