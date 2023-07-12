import argparse
from ase.calculators.vasp import Vasp
from ase.io import read, write


def check_magmom(args):
    # THE LIST CASE
    magmom = 0
    try:
        magmom = eval(args.magmom)
    except:
        raise Exception('MAGMOM should be a python list!')
    if not type(magmom) == list:
        raise Exception('MAGMOM format is wrong!')
    if len(magmom) != args.natoms:
        raise Exception('Length of the MAGMOM list should be == number of atoms')
    for i in magmom:
        if not type(i) == int:
           raise Exception('MAGMOM list should only contain integers!') 
    return magmom


def parse_args():
    parser = argparse.ArgumentParser(description="Create VASP inputs using ASE")

    # Structure parameters from file -f or --file
    def poscar_file(x):
        with open(x, 'r') as f:
            return read(f)

    parser.add_argument("poscar", type=poscar_file, help="Structure file")

    # Electronic parameters
    parser.add_argument("--encut", type=float, help="Cutoff energy for plane waves")
    parser.add_argument("--ediff", type=float, help="Energy convergence criterion")
    parser.add_argument("--ediffg", type=float, help="Force convergence criterion")
    parser.add_argument("--algo",
                        type=str,
                        choices=["Normal", "Fast", "VeryFast"],
                        help="Electronic minimization algorithm")
    parser.add_argument("--isif",
                        type=int,
                        choices=[0, 1, 2, 3, 4, 5, 6, 7],
                        help="Ionic relaxation method")
    # Add more arguments as needed
    parser.add_argument("--nsw", type=int, help="Number of ionic steps")
    parser.add_argument("--ibrion", type=int, help="Ionic relaxation algorithm")
    parser.add_argument("--potim", type=float, help="Ionic relaxation time step")

    # add nelm
    parser.add_argument("--nelm", type=int, help="Number of electronic steps")

    # ispin
    parser.add_argument("--ispin", type=int, help="Spin polarization")

    # Kpoints parameters
    parser.add_argument("--kpts",
                        type=int,
                        nargs=3,
                        default=[1, 1, 1],
                        help="Number of kpoints along each reciprocal lattice vector")
    parser.add_argument("--kgamma", 
                        action="store_true", 
                        help="Use Gamma-centered kpoint grid")
    parser.add_argument("--linemode", 
                        action="store_true", 
                        help="Use line mode for band structure")

    # Exchange-correlation parameters
    parser.add_argument("--xc", 
                        type=str, 
                        default="pbe", 
                        help="Exchange-correlation functional")

    # Parallelization parameters
    parser.add_argument("--npar", type=int, help="Number of cores to use")

    # IO parameters
    parser.add_argument("--lwave", action="store_true", help="Write WAVECAR")
    parser.add_argument("--lcharg", action="store_true", help="Write CHGCAR")
    parser.add_argument("--lreal",
                        type=str,
                        choices=["Auto", "None", "A", "B", "C"],
                        help="Type of real-space projection")
    parser.add_argument("--laechg", 
                        action="store_true", 
                        help="Write AECCAR0 and AECCAR2")

    # Precison parameters
    parser.add_argument("--prec", 
                        type=str, 
                        choices=["N", "L", "M", "H", "A"], 
                        help="Precision")

    # Symmetry parameters
    parser.add_argument("--symprec", type=float, help="Symmetry precision")
    parser.add_argument("--isym", type=int, choices=[-1, 0, 1, 2, 3])

    # Charge density parameters
    parser.add_argument("--icharg",
                        type=int,
                        choices=[0, 1, 2, 4, 10, 11, 12],
                        help="Charge density initialization")

    # Spin orbit coupling parameters
    parser.add_argument("--lsorbit", action="store_true", help="Spin orbit coupling")

    # Smearing parameters
    parser.add_argument("--ismear", 
                        type=int, 
                        choices=[-5, -4, -3, -2, -1, 0, 1], 
                        help="Smearing method")
    parser.add_argument("--sigma", type=float, help="Smearing width")

    # MAGMOM
    parser.add_argument("--magmom", help="List of magnetic moments. [Order matters]")
    args = parser.parse_args()
    # Process arguments
    args.atoms = args.poscar
    args.natoms = args.atoms.get_global_number_of_atoms()
    args.magmom = check_magmom(args)

    return args


def create_vasp_inputs(args):
    # Read the structure from the specified file
    atoms = args.atoms

    # Use the specified arguments to create the Vasp calculator
    calc = Vasp(
        atoms=args.atoms,
        encut=args.encut,
        ediff=args.ediff,
        ediffg=args.ediffg,
        algo=args.algo,
        isif=args.isif,
        kpts=args.kpts,
        ismear=args.ismear,
        sigma=args.sigma,
        xc=args.xc,
        npar=args.npar,
        lwave=args.lwave,
        lcharg=args.lcharg,
        lreal=args.lreal,
        laechg=args.laechg,
        prec=args.prec,
        symprec=args.symprec,
        isym=args.isym,
        icharg=args.icharg,
        lsorbit=args.lsorbit,
        nelm=args.nelm,
        ibrion=args.ibrion,
        nsw=args.nsw,
        potim=args.potim,
        ispin=args.ispin,
        magmom=args.magmom
    )

    atoms.calc = calc
    calc.write_input(atoms)


def main():
    args = parse_args()
    create_vasp_inputs(args)


if __name__ == "__main__":
    main()
