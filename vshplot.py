import argparse
from ase.calculators.vasp import Vasp
from ase.io import read, write


def parse_args():
    parser = argparse.ArgumentParser(description="Create plots of VASP results using PyProcar")

    # location




    args = parser.parse_args()
    # Process arguments
    args.atoms = read(args.poscar)
    args.poscar.close()
    return args


def create_vasp_inputs(args):
    # Read the structure from the specified file
    atoms = args.atoms

    # Use the specified arguments to create the Vasp calculator
    calc = Vasp(
        atoms=atoms
    )

    atoms.calc = calc
    calc.write_input(atoms)


def main():
    args = parse_args()
    create_vasp_inputs(args)


if __name__ == "__main__":
    main()
