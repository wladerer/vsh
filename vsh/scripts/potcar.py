from ase.io import read, write
from pymatgen.io.vasp.inputs import Poscar, Potcar


def get_atoms(args):
    """Creates ASE atoms object from a file"""

    atoms = read(args.input)

    return atoms


def potcar_from_structure(file: str, functional: str) -> Potcar:
    """Creates a POTCAR object from a structure file"""
    poscar = Poscar.from_file(file, check_for_POTCAR=False)

    # get a list of the symbols
    symbols = poscar.site_symbols

    potcar = Potcar(symbols=symbols, functional=functional)

    return potcar


def potcar_from_symbols(symbols: list, functional: str) -> Potcar:
    """Creates a POTCAR object from a list of symbols"""
    potcar = Potcar(symbols=symbols, functional=functional)

    return potcar


def write_potcar(potcar: Potcar, output: str | None = None) -> Potcar:
    """Writes a POTCAR file"""

    if not output:
        print(potcar.__str__())

    else:
        potcar.write_file(f"{output}")

    return potcar


def run(args):
    if args.structure:
        potcar = potcar_from_structure(args.structure, args.functional)
    elif args.symbols:
        potcar = potcar_from_symbols(args.symbols, args.functional)
    else:
        raise ValueError("No structure or symbols provided")

    write_potcar(potcar, args.output)

    return None
