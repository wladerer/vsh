def analysis(subparsers):
    subp_analysis = subparsers.add_parser("analysis", help="Analyze structure using ASE and pymatgen utilities")

    # Structure parameters from file -f or --file
    subp_analysis.add_argument("-f", "--file", type=str, help="Specify structure file", default="vasprun.xml")
    subp_analysis.add_argument(
        "--volume", help="Prints the volume of the structure", action="store_true"
    )
    subp_analysis.add_argument("--conflicts", type=float, help="Prints the conflicting atoms")
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
    subp_analysis.add_argument(
        "--positions", help="Prints the positions of the atoms"
    )
    subp_analysis.add_argument(
        "--converged", action="store_true", help="Prints if the structure is converged")


def bands(subparsers):
    subp_band = subparsers.add_parser('bands', help='Plot band structure')

    subp_band.add_argument('-e','--elimit', type=float, nargs='+', default=[-2,2], help='Range of energy to plot')
    subp_band.add_argument('-m', '--mode', type=str, default='parametric', help='Plotting mode')
    subp_band.add_argument('--orbitals', nargs='+', default=None, help='Orbitals to plot')
    subp_band.add_argument('--spins', type=int, nargs='+', default=None, help='Spins to plot')
    subp_band.add_argument('--atoms', type=int, nargs='+', default=None, help='Atoms to plot')
    subp_band.add_argument('--cmap', type=str, default='cool', help='Color map')
    subp_band.add_argument('--clim', type=float, nargs='+', default=[0,1], help='Color map limits')
    subp_band.add_argument('--code', type=str, default='vasp', help='Code used to generate the data')
    subp_band.add_argument('--dirname', type=str, default='.', help='Directory where the data is stored')
    subp_band.add_argument('-o', '--output', type=str, default=None, help='Output file name')
    subp_band.add_argument('--fermi', type=float, default=None, help='Fermi energy (eV)')
    subp_band.add_argument('--dpi', type=int, default=800, help='DPI of the output file')


def db(subparsers):
    """Parse command line arguments"""
    subp_db = subparsers.add_parser(
        "db", help="Interact with ASE database using extended vsh logic"
    )
    subp_db.add_argument(
        "-f", "--file", default="vasprun.xml", type=str, help="vasprun.xml file"
    )
    subp_db.add_argument(
        "-d", "--database", type=str, help="Database file", required=True
    )


def freeze(subparsers):
    subp_freeze = subparsers.add_parser("freeze", help="Freeze atoms using ASE")

    subp_freeze.add_argument(
        "-f", "--filename", type=str, help="Structure file", required=True
    )
    subp_freeze.add_argument(
        "-i",
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
    # sort atoms
    subp_freeze.add_argument("--sort", action="store_true", help="Sort atoms")
    subp_freeze.add_argument(
        "--zrange", type=float, nargs=2, help="Freeze atoms with zmin < z < zmax"
    )


def inputs(subparsers):
    subp_inputs = subparsers.add_parser("inputs", help="Generate VASP inputs")

    subp_inputs.add_argument("-f", "--file", type=str, default=None, help="Input file")
    subp_inputs.add_argument("-d", "--directory", type=str, default=".", help="Directory to write VASP inputs to")
    subp_inputs.add_argument("--potcar", type=bool, default=False, help="Write POTCAR file")
    subp_inputs.add_argument("-k", "--kpoints", type=int, nargs=3, default=None, help="Writes gamma centered KPOINTS file")
    subp_inputs.add_argument("-i", "--incar", type=str, default=None, help="INCAR file type", choices=["bulk", "slab", "band", "single-point", "band-soc", "band-slab-soc"])
    subp_inputs.add_argument("--kpath", type=int, default=None, help="KPOINTS file for band structure calculation")
    subp_inputs.add_argument("--symprec", type=float, default=None, help="Symmetry precision for SeekPath algorithm")
    subp_inputs.add_argument("--sort", action="store_true", help="Sort atoms in POSCAR file")
    subp_inputs.add_argument("--freeze", type=str, default=None, help="Freeze atoms in POSCAR file")
    subp_inputs.add_argument("--mp-poscar", type=str, default=None, help="Get POSCAR file from Materials Project")
    subp_inputs.add_argument("--primitive", type=bool, default=False, help="Get primitive POSCAR file from Materials Project")
    subp_inputs.add_argument("-o", "--output", help="Name of output file")

def slab(subparsers):
    subp_slabgen = subparsers.add_parser(
        "slab", help="Generate slabs from structure using pymatgen"
    )

    subp_slabgen.add_argument("-f", "--file", type=str, help="Structure file", required=True)
    subp_slabgen.add_argument(
        "-m",
        "--miller-plane",
        type=int,
        nargs=3,
        default=[0, 0, 1],
        help="Miller plane",
    )
    subp_slabgen.add_argument("-o", "--output", type=str, help="Output file basename")
    subp_slabgen.add_argument("--sort", help="Sort atoms")
    subp_slabgen.add_argument("-v", "--vacuum", type=float, default=15.0, help="Vacuum size")
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
    subp_slabgen.add_argument("--primitive", default=False, help="Create primitive cell")
    subp_slabgen.add_argument("-c", "--center-slab", default=True, help="Center the slab")
    subp_slabgen.add_argument(
        "-u",
        "--in-unit-planes",
        default=False,
        type=bool,
        help="Specify zmin in multiples of miller plane spacing",
    )
    subp_slabgen.add_argument(
        "--freeze", default=5, type=float, help="Freeze the bottom layer of the slab"
    )


def setup(subparsers):
    for script in analysis, bands, db, freeze, inputs, slab:
        script(subparsers)

