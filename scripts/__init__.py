import argparse


def analysis(subparsers):
    subp_analysis = subparsers.add_parser(
        "analysis", help="Analyze structure using ASE and pymatgen utilities"
    )

    # Structure parameters from file -f or --file
    subp_analysis.add_argument(
        "-i", "--input", type=str, help="Specify structure file", default="vasprun.xml"
    )
    subp_analysis.add_argument(
        "--volume", help="Prints the volume of the structure", action="store_true"
    )
    subp_analysis.add_argument(
        "--conflicts", type=float, help="Prints the conflicting atoms"
    )
    subp_analysis.add_argument(
        "--cell", help="Prints the unit cell dimensions", action="store_true"
    )
    subp_analysis.add_argument(
        "--params",
        help="Prints the unit cell parameters (a,b,c) of the structure",
        action="store_true",
    )
    subp_analysis.add_argument(
        "--symmetry",
        help="Prints the space group number and symbol",
        action="store_true",
    )
    subp_analysis.add_argument(
        "--energy", help="Prints the energy of the structure", action="store_true"
    )
    subp_analysis.add_argument(
        "--vacuum", help="Prints the vacuum of the structure", action="store_true"
    )
    subp_analysis.add_argument("--positions", help="Prints the positions of the atoms")
    subp_analysis.add_argument(
        "-c",
        "--converged",
        action="store_true",
        help="Prints if the structure is converged",
    )


def band(subparsers):
    subp_band = subparsers.add_parser("bands", help="Plot band structure")

    subp_band.add_argument(
        "-e",
        "--elimit",
        type=float,
        nargs="+",
        default=[-2, 2],
        help="Range of energy to plot",
    )
    subp_band.add_argument(
        "-m", "--mode", type=str, default="parametric", help="Plotting mode"
    )
    subp_band.add_argument(
        "--orbitals", nargs="+", default=None, help="Orbitals to plot"
    )
    subp_band.add_argument(
        "--spins", type=int, nargs="+", default=None, help="Spins to plot"
    )
    subp_band.add_argument(
        "--atoms", type=int, nargs="+", default=None, help="Atoms to plot"
    )
    subp_band.add_argument("--cmap", type=str, default="cool", help="Color map")
    subp_band.add_argument(
        "--clim", type=float, nargs="+", default=[0, 1], help="Color map limits"
    )
    subp_band.add_argument(
        "--code", type=str, default="vasp", help="Code used to generate the data"
    )
    subp_band.add_argument(
        "--dirname", type=str, default=".", help="Directory where the data is stored"
    )
    subp_band.add_argument(
        "-o", "--output", type=str, default=None, help="Output file name"
    )
    subp_band.add_argument(
        "--fermi", type=float, default=None, help="Fermi energy (eV)"
    )
    subp_band.add_argument(
        "--dpi", type=int, default=800, help="DPI of the output file"
    )


def db(subparsers):
    """Parse command line arguments"""
    subp_db = subparsers.add_parser(
        "db", help="Interact with ASE database using extended vsh logic"
    )
    subp_db.add_argument(
        "-i", "--input", default="vasprun.xml", type=str, help="vasprun.xml file"
    )
    subp_db.add_argument("database", type=str, help="Database file")


def freeze(subparsers):
    subp_freeze = subparsers.add_parser("freeze", help="Freeze atoms using ASE")

    subp_freeze.add_argument(
        "-i", "--input", type=str, help="Structure file", required=True
    )
    subp_freeze.add_argument(
        "--indices",
        type=int,
        nargs="+",
        default=None,
        help="Atom indices to freeze",
    )
    subp_freeze.add_argument("-t", "--type", type=str, help="Atom type to freeze")
    subp_freeze.add_argument(
        "-z", "--zmax", type=float, help="Freeze atoms with z < zmax"
    )
    subp_freeze.add_argument("-o", "--output", type=str, help="Output file name")
    subp_freeze.add_argument("--sort", action="store_true", help="Sort atoms")
    subp_freeze.add_argument(
        "--zrange", type=float, nargs=2, help="Freeze atoms with zmin < z < zmax"
    )


def input(subparsers):
    subp_inputs = subparsers.add_parser("input", help="Generate VASP inputs")

    subp_inputs.add_argument("-i", "--input", type=str, default=None, help="Structure input file")
    subp_inputs.add_argument(
        "-d",
        "--directory",
        type=str,
        default=".",
        help="Directory to write VASP inputs to",
    )
    subp_inputs.add_argument(
        "--potcar", type=bool, default=False, help="Write POTCAR file"
    )
    subp_inputs.add_argument(
        "-k",
        "--kpoints",
        type=int,
        nargs=3,
        default=None,
        help="Writes gamma centered KPOINTS file",
    )
    subp_inputs.add_argument(
        "--incar",
        type=str,
        default=None,
        help="INCAR file type",
        choices=["bulk", "slab", "band", "single-point", "band-soc", "band-slab-soc"],
    )
    subp_inputs.add_argument(
        "--kpath",
        type=int,
        default=None,
        help="KPOINTS file for band structure calculation",
    )
    subp_inputs.add_argument(
        "--symprec",
        type=float,
        default=None,
        help="Symmetry precision for SeekPath algorithm",
    )
    subp_inputs.add_argument(
        "--sort", action="store_true", help="Sort atoms in POSCAR file"
    )
    subp_inputs.add_argument(
        "--freeze", type=str, default=None, help="Freeze atoms in POSCAR file"
    )
    subp_inputs.add_argument(
        "--mp-poscar",
        type=str,
        default=None,
        help="Get POSCAR file from Materials Project",
    )
    subp_inputs.add_argument(
        "--primitive",
        type=bool,
        default=False,
        help="Get primitive POSCAR file from Materials Project",
    )
    subp_inputs.add_argument("-o", "--output", help="Name of output file")


def slab(subparsers):
    subp_slabgen = subparsers.add_parser(
        "slab", help="Generate slabs from structure using pymatgen"
    )

    subp_slabgen.add_argument("structure", type=str, help="Structure file"
    )
    subp_slabgen.add_argument(
        "-m",
        "--miller-plane",
        type=int,
        nargs=3,
        default=[0, 0, 1],
        help="Miller plane",
    )
    subp_slabgen.add_argument("-o", "--output", type=str, help="Output file basename")
    subp_slabgen.add_argument("--sort", action='store_true', help="Sort atoms")
    subp_slabgen.add_argument(
        "-v", "--vacuum", type=float, default=15.0, help="Vacuum size"
    )
    subp_slabgen.add_argument(
        "-s",
        "--symmetric",
        type=bool,
        default=True,
        help="Ensure that the faces of the slab are symmetric",
    )
    subp_slabgen.add_argument(
        "-t",
        "--thickness",
        default=3.0,
        help="Minimum slab thickness in Angstrom or multiples of miller plane spacing",
    )
    subp_slabgen.add_argument(
        "--primitive", default=False, help="Create primitive cell"
    )
    subp_slabgen.add_argument(
        "-c", "--center-slab", default=True, help="Center the slab"
    )
    subp_slabgen.add_argument(
        "-u",
        "--in-unit-planes",
        action='store_true',
        default=False,
        help="Specify zmin in multiples of miller plane spacing",
    )
    subp_slabgen.add_argument(
        "--freeze", default=5, type=float, help="Freeze the bottom layer of the slab"
    )


def schedule(subparsers):
    subp_schedule = subparsers.add_parser(
        "schedule", help="Schedule jobs on a supercomputer"
    )

    subp_schedule.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w", encoding="utf-8"),
        help="Submission script file name",
    )

    subp_schedule.add_argument(
        "-n", "--nodes", type=int, default=1, help="Number of nodes"
    )
    subp_schedule.add_argument(
        "-p", "--ppn", type=int, default=1, help="Processors per node"
    )
    subp_schedule.add_argument(
        "-t", "--walltime", type=str, default="00:30:00", help="Walltime"
    )
    subp_schedule.add_argument(
        "-q", "--queue", type=str, default="standard", help="Queue"
    )
    subp_schedule.add_argument("-a", "--account", type=str, help="Account")
    subp_schedule.add_argument("-m", "--mail", type=str, help="Email address")
    subp_schedule.add_argument(
        "-e", "--email-type", type=str, default="", help="Email type"
    )
    subp_schedule.add_argument(
        "-d",
        "--directives",
        type=str,
        default="",
        nargs="+",
        help="Additional directives",
    )
    subp_schedule.add_argument(
        "-j", "--job-name", type=str, default="", help="Job name"
    )
    subp_schedule.add_argument("--pbs", action="store_true", help="Use PBS")
    subp_schedule.add_argument("--slurm", action="store_true", help="Use SLURM")


def manage(subparsers):
    subp_manage = subparsers.add_parser("manage", help="Manage VASP calculations")

    subp_manage.add_argument(
        "--archive", action="store_true", help="Archive output files"
    )
    subp_manage.add_argument("--copy", action="store_true", help="Copy output files")
    subp_manage.add_argument(
        "-e",
        "--exclude",
        type=list,
        nargs="+",
        default=[],
        help="Exclude files from archive or copy",
    )
    subp_manage.add_argument(
        "-d", "--destination", type=str, default=None, help="Destination for copy"
    )
    subp_manage.add_argument(
        "-o", "--output", type=str, default=None, help="Output file name"
    )
    subp_manage.add_argument(
        "-w",
        "--rename-contcar",
        action="store_true",
        help="Rename CONTCAR to POSCAR when copied",
    )
    subp_manage.add_argument(
        "-s", "--snapshot", type=str, help="Input file to snapshot"
    )


def adsorb(subparsers):
    subp_adsorb = subparsers.add_parser("adsorb", help="Generate adsorbed structures")

    subp_adsorb.add_argument("-i", "--input", type=str, default=None, help="Input file")
    subp_adsorb.add_argument(
        "-a", "--adsorbate", type=str, default=None, help="Adsorbate file"
    )
    subp_adsorb.add_argument(
        "-z",
        "--distance",
        type=float,
        default=1.0,
        help="Distance between adsorbate and surface",
    )
    subp_adsorb.add_argument(
        "-m", "--min-z", type=float, default=5.0, help="Minimum z value for freezing"
    )
    subp_adsorb.add_argument(
        "-c",
        "--coverage",
        type=int,
        nargs=3,
        default=[1, 1, 1],
        help="Adsorbate coverage",
    )
    subp_adsorb.add_argument(
        "-o", "--output", type=str, default=None, help="Output basename"
    )


def setup(subparsers):
    for script in analysis, band, db, freeze, input, slab, schedule, manage, adsorb:
        script(subparsers)
