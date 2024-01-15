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
    subp_band = subparsers.add_parser("band", help="Plot band structure")

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


def incar(subparsers):
    subp_incar = subparsers.add_parser("incar", help="Generate and update INCAR files")
    
    subp_incar.add_argument("--write", choices=['bulk', 'bader', 'slab', 'band-slab', 'band', 'single-point', 'single-point-slab', 'single-point-slab-soc'], help="Write an INCAR file from the defaults in incar.json")
    subp_incar.add_argument("-i", "--input", type=str, help="INCAR file path")
    subp_incar.add_argument("-u", "--update", help="Update an INCAR file with the specified tag value pair", nargs=2, type=str)
    subp_incar.add_argument("-o", "--output", type=str, help="Output file name")
    

def poscar(subparsers):
    subp_poscar = subparsers.add_parser("poscar", help="Generate and update POSCAR files")
    subp_poscar.add_argument("-i", "--input", type=str, help="Structure file")
    subp_poscar.add_argument("--mp-poscar", type=str, help="Materials Project code")
    subp_poscar.add_argument("-p", "--primitive", action='store_true', help="Use primitive cell")
    subp_poscar.add_argument("-o", "--output", type=str, help="Output file name")
    subp_poscar.add_argument("--sort", action='store_true', help="Sort atoms")
    subp_poscar.add_argument("-c", "--convert", action='store_true', help="Convert any structure file to POSCAR")
    subp_poscar.add_argument("--super", nargs=3, type=int, help="Generate a supercell")
    subp_poscar.add_argument("-l", "--list", action='store_true', help="List the positions of the atoms")
    
def potcar(subparsers):
    subp_potcar = subparsers.add_parser("potcar", help="Generate and update POTCAR files")
    subp_potcar.add_argument("-s", "--structure", type=str, help="Structure file")
    subp_potcar.add_argument("-e", "--elements", nargs='+', type=str, help="Elements")
    subp_potcar.add_argument("-o", "--output", type=str, help="Output file name")
        
    
def kpoints(subparsers):
    subp_kpoints = subparsers.add_parser("kpoints", help="Generate and update KPOINTS files")
    
    subp_kpoints.add_argument("--path", type=int, help="Generate a KPOINTS file for a line mode calculation")
    subp_kpoints.add_argument("-i", "--input", type=str, help="Structure file")
    subp_kpoints.add_argument("--plane", type=int, help="Generate a KPOINTS file for a 2D plane mode calculation")
    subp_kpoints.add_argument("--mesh", nargs=3, type=int, help="Generate a KPOINTS file for a mesh mode calculation")
    subp_kpoints.add_argument("--mesh-type", choices=['gamma', 'monkhorst-pack'], default="gamma", help="Mesh type")
    subp_kpoints.add_argument("-o", "--output", type=str, help="Output file name")
    # subp_kpoints.add_argument("--hybrid", action='store_true', help="Update a KPOINTS file for a hybrid calculation")
    # subp_kpoints.add_argument("--step", type=float, default=0.1, help="Step size for hybrid mesh")
    # subp_kpoints.add_argument("--weight", type=int, default=0, help="Weight for hybrid mesh")

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
    subp_manage.add_argument("--mkvdir", action="store_true", help="Create a directory for each structure in the current directory")
    subp_manage.add_argument("-i", "--input", nargs='+', type=str, help="Input file(s)")


def adsorb(subparsers):
    subp_adsorb = subparsers.add_parser("adsorb", help="Generate adsorbed structures")

    subp_adsorb.add_argument("input", type=str, help="Input file")
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
        "--freeze", type=float, default=5.0, help="Minimum z value for freezing"
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

def alchemy(subparsers):

    subp_alchemy = subparsers.add_parser('alchemy', help='Manipulate structures and their atoms')
    subp_alchemy.add_argument('input', help='Input file')
    subp_alchemy.add_argument('-d', '--delete', help='Delete atoms', action='store_true')
    subp_alchemy.add_argument('--freeze', help='Freeze atoms', action='store_true')
    subp_alchemy.add_argument('--swap', help='Swap atoms', action='store_true')
    subp_alchemy.add_argument('--rattle', help='Perturb the sites of a structure', action='store_true')
    subp_alchemy.add_argument('-o', '--output', help='Output file')
    subp_alchemy.add_argument('-i', '--index', help='Indices of atoms to select', nargs='+', type=int)
    subp_alchemy.add_argument('-t', '--type', help='Type of atoms to select', nargs='+', type=str)
    subp_alchemy.add_argument('-z', help='Z position of atoms to freeze', type=float)
    subp_alchemy.add_argument('--direction', help='Direction of atoms to freeze', type=str, choices=['above', 'below'])
    subp_alchemy.add_argument('--range', help='Range of atoms to freeze', nargs=2, type=float)


def cohp(subparsers):
    subp_cohp = subparsers.add_parser("cohp", help="Plot COHPs")

    subp_cohp.add_argument(
        "input",
        type=str,
        nargs="+",
        help="Input file or directory containing COHP or COHP files",
    )
    subp_cohp.add_argument(
        "-c",
        "--cobi",
        action="store_true",
        help="Use COBIs instead of COHPs",
    )
    subp_cohp.add_argument(
        "--label",
        type=str,
        default="",
        help="Label for the COHP or COBIs",
    )
    subp_cohp.add_argument(
        "-t",
        "--title",
        type=str,
        default="",
        help="Title for the plot",
    )
    subp_cohp.add_argument(
        "-o",
        "--output",
        type=str,
        nargs="+",
        help="Output file name(s)",
    )
    subp_cohp.add_argument(
        "-d",
        "--dpi",
        type=int,
        default=800,
        help="DPI of the output file",
    )
    subp_cohp.add_argument(
        "-x",
        "--xlim",
        type=float,
        nargs=2,
        default=None,
        help="X-axis limits",
    )
    subp_cohp.add_argument(
        "-y",
        "--ylim",
        type=float,
        nargs=2,
        default=None,
        help="Y-axis limits",
    )
    subp_cohp.add_argument(
        "--integrated",
        action="store_true",
        help="Plot the integrated COHPs",
    )
    subp_cohp.add_argument(
        "-p",
        "--plot",
        action="store_true",
        help="Plot the COHPs",
    )
    subp_cohp.add_argument(
        "-l",
        "--list",
        action="store_true",
    )
    subp_cohp.add_argument(
        "--pickle",
        action="store_true",   
    )
    subp_cohp.add_argument(
        "--graph",
        action="store_true",
    )

def procar(subparsers):
    '''Parser for procar files'''

    subp_procar = subparsers.add_parser('procar', help='Reads projected eigenvalue information from vasprun.xml or procar.vsh pickle files (0 based index btw)')
    subp_procar.add_argument('input', help='Either vasprun.xml or vsh pickle file')
    subp_procar.add_argument('-k', '--kpoint', help='Kpoint of interest')
    subp_procar.add_argument('-b', '--band', help='Band of interest')
    subp_procar.add_argument('-i', '--ion', help='Ion of interest')
    subp_procar.add_argument('--orbital', help='Orbital of interest')
    subp_procar.add_argument('--occupation', help='Occupation of interest')
    subp_procar.add_argument('-e', '--energy', help='Energy of interest')
    subp_procar.add_argument('-s', '--spin', help='Spin channel of interest')
    subp_procar.add_argument('-o', '--output', help='Output filename (either pickle file or queried results)')
    subp_procar.add_argument('-d', '--describe', action='store_true', help='Provides a brief description of the projected eigenvalues data')
    subp_procar.add_argument('--efermi', help='Reference Fermi Energy', type=float, default=0.0)

    #add argument group for file handling 
    file_handling = subp_procar.add_argument_group('file handling')
    file_handling.add_argument('-p', '--pickle', action='store_true', help='Write projected eigenvalues from a vasprun.xml file to a pickle file')

    #add argument group for plotting
    plotting = subp_procar.add_argument_group('Band Plotting')
    plotting.add_argument('--plot', action='store_true')
    plotting.add_argument('--kplot', help='Plot orbital variation of a single band',action='store_true')
    plotting.add_argument('--iplot', help='Plot compositional variation of a single band', action='store_true')
    plotting.add_argument('--erange', nargs=2, type=float, help='Energy range to plot')
    plotting.add_argument('--irange', nargs=2, type=int, help='Index range to plot')
    plotting.add_argument('--labels', nargs='+', type=str, help='Labels for the plot')


    #add argument group for kpoint analysis and plotting
    kpoint_analysis = subp_procar.add_argument_group('kpoint analysis')
    kpoint_analysis.add_argument('-a', '--analyze', help='Kpoint analysis of a specific kpoint and band', action='store_true')


def setup(subparsers):
    for script in adsorb, alchemy, analysis, band, cohp, db, incar, kpoints, manage, poscar, procar, slab:
        script(subparsers)
