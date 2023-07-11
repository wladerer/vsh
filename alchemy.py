import argparse
from ase.io import read, write


def convert_atoms():
    """Convert atoms of one type to another"""
    parser = argparse.ArgumentParser(description="Convert atoms using ASE")

    parser.add_argument("-f", "--file", type=str, help="Structure file")
    parser.add_argument("-n", "--new", type=str, help="New atom type")
    parser.add_argument(
        "-i", "--indices", type=int, nargs="+", help="Atom indices to convert"
    )
    parser.add_argument("-t", "--type", type=str, help="Atom type to convert")
    parser.add_argument(
        "-o", "--output", type=str, default="converted.vasp", help="Output file name"
    )
    parser.add_argument("--sort", action="store_true", help="Sort atoms")
    args = parser.parse_args()
    atoms = read(args.file)

    if args.type:
        indices = [i for i, atom in enumerate(atoms) if atom.symbol == args.type]
        args.indices = list(set(indices))

    for i in args.indices:
        atoms[i].symbol = args.new

    write(args.output, atoms, vasp5=True, sort=args.sort)


if __name__ == "__main__":
    convert_atoms()
