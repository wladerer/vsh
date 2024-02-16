#!/usr/bin/env python3

import os

from ase.db import connect
from ase.io import read
from pymatgen.io.vasp.outputs import Vasprun


def check_for_vasprun(file: str) -> bool:
    """Checks if a vasprun.xml file exists and is valid"""
    is_file = os.path.isfile(file)

    if not is_file:
        raise ValueError(f"{file} not found")


def handle_kpoints(kpoints: list[tuple]) -> str:
    """Handles kpoints returned by pymatgen"""
    if len(kpoints) == 1:
        # this is an automatic generated mesh, just return the value as a string
        return str(kpoints[0])
    else:
        # this is a manual mesh, return the values as a string
        return str(kpoints)


def get_metadata(file: str) -> dict:
    """Returns metadata from vasprun.xml file"""
    # check for vasprun.xml file
    check_for_vasprun(file)
    vasprun = Vasprun(
        file,
        parse_dos=False,
        parse_eigen=False,
        parse_projected_eigen=False,
        parse_potcar_file=False,
    )

    spin = vasprun.parameters["ISPIN"]
    soc = vasprun.parameters["LSORBIT"]
    xc = vasprun.parameters["GGA"]
    kpoints = handle_kpoints(vasprun.kpoints.kpts)
    converged_ionic = vasprun.converged_ionic
    converged_electronic = vasprun.converged_electronic

    # get the path of the calculation
    path = os.path.abspath(file)
    path = os.path.dirname(path)

    metadata = {
        "spin": spin,
        "soc": soc,
        "xc": xc,
        "kpoints": kpoints,
        "ionic": converged_ionic,
        "electronic": converged_electronic,
        "path": path,
    }

    return metadata


def update_ase_db(vasprun_file: str, database: str):
    """Writes atoms and metadata to a database"""
    atoms = read(vasprun_file)
    metadata = get_metadata(vasprun_file)
    db = connect(database)
    db.write(
        atoms,
        xc=metadata["xc"],
        spin=metadata["spin"],
        soc=metadata["soc"],
        kpoints=metadata["kpoints"],
        ionic=metadata["ionic"],
        electronic=metadata["electronic"],
        path=metadata["path"],
    )

    return None


def setup_args(subparsers):
    """Parse command line arguments"""
    subp_db = subparsers.add_parser(
        "db", help="Interact with ASE database using extended vsh logic"
    )
    subp_db.add_argument(
        "-i", "--input", default="vasprun.xml", type=str, help="vasprun.xml file"
    )
    subp_db.add_argument("database", type=str, help="Database file", required=True)


def run(args):
    """Run the db command"""
    update_ase_db(args.input, args.database)
