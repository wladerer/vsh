import argparse


def is_number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


class MeshAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) not in [1, 3]:
            raise argparse.ArgumentError(
                self, "argument --mesh requires 1 or 3 integers"
            )
        setattr(namespace, self.dest, values)


def analysis(subparsers):
    subp_analysis = subparsers.add_parser(
        "analysis", help="Analyze structure using ASE and pymatgen utilities"
    )
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

    subp_band.add_argument("--filter", action="store_true", help="Filter the data")


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

    subp_incar.add_argument(
        "--write",
        choices=[
            "bulk",
            "bader",
            "slab",
            "band-slab",
            "band-slab-soc",
            "band",
            "single-point",
            "single-point-slab",
            "single-point-slab-soc",
        ],
        help="Write an INCAR file from the defaults in incar.json",
    )
    subp_incar.add_argument("-i", "--input", type=str, help="INCAR file path")
    subp_incar.add_argument(
        "-u",
        "--update",
        help="Update an INCAR file with the specified tag value pair",
        nargs=2,
        type=str,
    )
    subp_incar.add_argument("-o", "--output", type=str, help="Output file name")
    subp_incar.add_argument("-t", "--tag-info", type=str, help="Get help on a VASP tag")


def poscar(subparsers):
    subp_poscar = subparsers.add_parser(
        "poscar", help="Generate and update POSCAR files"
    )
    subp_poscar.add_argument(
        "input", type=str, help="Structure file or Materials Project ID"
    )
    subp_poscar.add_argument(
        "--rdf",
        action="store_true",
        help="Plot the radial distribution function of a structure",
    )
    subp_poscar.add_argument(
        "-p", "--primitive", action="store_true", help="Use primitive cell"
    )
    subp_poscar.add_argument("-o", "--output", type=str, help="Output file name")
    subp_poscar.add_argument("--sort", action="store_true", help="Sort atoms")
    subp_poscar.add_argument(
        "-c",
        "--convert",
        action="store_true",
        help="Convert any structure file to POSCAR",
    )
    subp_poscar.add_argument("--super", nargs=3, type=int, help="Generate a supercell")
    subp_poscar.add_argument(
        "-l", "--list", action="store_true", help="List the positions of the atoms"
    )
    subp_poscar.add_argument(
        "-d",
        "--dynamics",
        action="store_true",
        help="List atoms and their degrees of freedom",
    )
    subp_poscar.add_argument(
        "--mp",
        action="store_true",
        help="Retrieve (relaxed, conventional) poscar from Materials Project API",
    )
    subp_poscar.add_argument(
        "--compare",
        nargs="+",
        type=str,
        help="Compare the radial distribution of multiple structures",
    )

    molecule = subp_poscar.add_argument_group("Molecular Tools")
    molecule.add_argument(
        "-b",
        "--box",
        action="store_true",
        help="Create a POSCAR for a molecule surrounded by vacuum",
    )
    molecule.add_argument(
        "-v", "--vacuum", type=float, default=12.0, help="Vacuum size"
    )
    molecule.add_argument(
        "-N",
        "--no-cross",
        action="store_true",
        help="Do not cross the periodic boundary",
        default=False,
    )


def potcar(subparsers):
    subp_potcar = subparsers.add_parser(
        "potcar", help="Generate and update POTCAR files"
    )
    subp_potcar.add_argument("-s", "--structure", type=str, help="Structure file")
    subp_potcar.add_argument("-e", "--elements", nargs="+", type=str, help="Elements")
    subp_potcar.add_argument("-o", "--output", type=str, help="Output file name")


def kpoints(subparsers):
    subp_kpoints = subparsers.add_parser(
        "kpoints", help="Generate and update KPOINTS files"
    )

    subp_kpoints.add_argument(
        "--path", type=int, help="Generate a KPOINTS file for a line mode calculation"
    )
    subp_kpoints.add_argument("-i", "--input", type=str, help="Structure file")
    subp_kpoints.add_argument(
        "--plane",
        type=int,
        help="Generate a KPOINTS file for a 2D plane mode calculation",
    )
    subp_kpoints.add_argument(
        "--mesh",
        nargs="*",
        type=is_number,
        help="Generate a KPOINTS file for a mesh mode calculation",
    )
    subp_kpoints.add_argument(
        "--mesh-type",
        choices=["gamma", "monkhorst", "automatic"],
        default="gamma",
        help="Mesh type",
    )
    subp_kpoints.add_argument("-o", "--output", type=str, help="Output file name")
    subp_kpoints.add_argument(
        "--mueller-grid",
        action="store_true",
        help="Generate generalized regular grid designed by the Muller group at John's Hopkins. Requires KpLib",
    )
    # subp_kpoints.add_argument("--hybrid", action='store_true', help="Update a KPOINTS file for a hybrid calculation")
    # subp_kpoints.add_argument("--step", type=float, default=0.1, help="Step size for hybrid mesh")
    # subp_kpoints.add_argument("--weight", type=int, default=0, help="Weight for hybrid mesh")


def slab(subparsers):
    subp_slabgen = subparsers.add_parser(
        "slab", help="Generate slabs from structure using pymatgen"
    )

    subp_slabgen.add_argument("input", type=str, help="Structure file")
    subp_slabgen.add_argument(
        "-m",
        "--miller-plane",
        type=int,
        nargs=3,
        default=[0, 0, 1],
        help="Miller plane",
    )
    subp_slabgen.add_argument("-o", "--output", type=str, help="Output file basename")
    subp_slabgen.add_argument("--sort", action="store_true", help="Sort atoms")
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
        action="store_true",
        default=False,
        help="Specify zmin in multiples of miller plane spacing",
    )
    subp_slabgen.add_argument(
        "--freeze", default=5, type=float, help="Freeze the bottom layer of the slab"
    )
    subp_slabgen.add_argument(
        "-r",
        "--reorient-lattice",
        action="store_true",
        help="Reorient the lattice",
        default=True,
    )
    subp_slabgen.add_argument(
        "-O", "--orthogonalize", action="store_true", help="Orthogonalize the a surface"
    )
    subp_slabgen.add_argument("-a", "--alpha", type=float, help="Alpha angle")
    subp_slabgen.add_argument("-b", "--beta", type=float, help="Beta angle")
    subp_slabgen.add_argument("-g", "--gamma", type=float, help="Gamma angle")
    subp_slabgen.add_argument(
        "-V", "--verbose", action="store_true", help="Verbose output"
    )
    subp_slabgen.add_argument(
        "--no-reduce",
        type=bool,
        help="Refrain from LLL reduce the lattice",
        default=False,
    )


def manage(subparsers):
    subp_manage = subparsers.add_parser("manage", help="Manage VASP calculations")

    subp_manage.add_argument(
        "input", type=str, help="Input vasprun.xml, pickle file, or VASP directory"
    )

    subp_manage.add_argument(
        "-a",
        "--archive",
        action="store_true",
        help="Archive output files in a pickle file",
    )
    subp_manage.add_argument(
        "-u",
        "--unarchive",
        action="store_true",
        help="Unarchive output files from a pickle file",
    )
    subp_manage.add_argument(
        "-v", "--validate", action="store_true", help="Validate input files"
    )
    subp_manage.add_argument(
        "-o", "--output", type=str, default=None, help="Output file name"
    )
    subp_manage.add_argument(
        "-s",
        "--snapshot",
        type=str,
        help="Take perspective view images of a structure file",
    )
    subp_manage.add_argument(
        "-n", "--note", type=str, help="Add a note to the pickle file"
    )
    subp_manage.add_argument(
        "-e",
        "--electronic-structure",
        action="store_true",
        help="Add projected electronic structure to the pickle file",
    )
    subp_manage.add_argument(
        "-R",
        "--reconstitute",
        action="store_true",
        help="Reconstitute VASP files from vasprun.xml",
    )


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
        default=1.2,
        help="Distance between adsorbate and surface",
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
        "-b", "--both", action="store_true", help="Adsorbate on both surfaces"
    )
    subp_adsorb.add_argument(
        "-o", "--output", type=str, default=None, help="Output basename"
    )
    subp_adsorb.add_argument(
        "-p",
        "--positions",
        choices=["all", "ontop", "bridge", "hollow"],
        default="all",
        help="Adsorption sites",
    )
    subp_adsorb.add_argument(
        "-P",
        "--plane",
        type=int,
        nargs=3,
        help="Miller plane required for adsorbing on both surfaces",
    )


def alchemy(subparsers):
    subp_alchemy = subparsers.add_parser(
        "alchemy", help="Manipulate structures and their atoms"
    )
    subp_alchemy.add_argument("input", help="Input file")
    subp_alchemy.add_argument(
        "-d", "--delete", help="Delete atoms", action="store_true"
    )
    subp_alchemy.add_argument("--freeze", help="Freeze atoms", action="store_true")
    subp_alchemy.add_argument("--swap", help="Swap atoms", action="store_true")
    subp_alchemy.add_argument(
        "--rattle", help="Perturb the sites of a structure", action="store_true"
    )
    subp_alchemy.add_argument("-o", "--output", help="Output file")
    subp_alchemy.add_argument(
        "-i", "--index", help="Indices of atoms to select", nargs="+", type=int
    )
    subp_alchemy.add_argument(
        "-t", "--type", help="Type of atoms to select", nargs="+", type=str
    )
    subp_alchemy.add_argument("-z", help="Z position of atoms to freeze", type=float)
    subp_alchemy.add_argument(
        "--direction",
        help="Direction of atoms to freeze",
        type=str,
        choices=["above", "below"],
    )
    subp_alchemy.add_argument(
        "--range", help="Range of atoms to freeze", nargs=2, type=float
    )


def cohp(subparsers):
    subp_cohp = subparsers.add_parser("cohp", help="Plot COHPs")
    subp_cohp.add_argument(
        "input",
        type=str,
        nargs="+",
        help="Input file or directory containing COHP or COHP files",
    )
    subp_cohp.add_argument(
        "-c", "--cobi", action="store_true", help="Use COBIs instead of COHPs"
    )
    subp_cohp.add_argument(
        "--label", type=str, default="", help="Label for the COHP or COBIs"
    )
    subp_cohp.add_argument(
        "-t", "--title", type=str, default="", help="Title for the plot"
    )
    subp_cohp.add_argument(
        "-o", "--output", type=str, nargs="+", help="Output file name(s)"
    )
    subp_cohp.add_argument(
        "-d", "--dpi", type=int, default=800, help="DPI of the output file"
    )
    subp_cohp.add_argument(
        "-x", "--xlim", type=float, nargs=2, default=None, help="X-axis limits"
    )
    subp_cohp.add_argument(
        "-y", "--ylim", type=float, nargs=2, default=None, help="Y-axis limits"
    )
    subp_cohp.add_argument(
        "--integrated", action="store_true", help="Plot the integrated COHPs"
    )
    subp_cohp.add_argument("-p", "--plot", action="store_true", help="Plot the COHPs")
    subp_cohp.add_argument("-l", "--list", action="store_true")
    subp_cohp.add_argument("--pickle", action="store_true")
    subp_cohp.add_argument("--graph", action="store_true")


def procar(subparsers):
    """Parser for procar files"""

    subp_procar = subparsers.add_parser(
        "procar",
        help="Reads projected eigenvalue information from vasprun.xml or procar.vsh pickle files (0 based index btw)",
    )
    subp_procar.add_argument("input", help="Either vasprun.xml or vsh pickle file")
    subp_procar.add_argument("-k", "--kpoint", help="Kpoint of interest")
    subp_procar.add_argument("-b", "--band", help="Band of interest")
    subp_procar.add_argument(
        "-i", "--ions", help="Ion(s) of interest", type=int, nargs="+"
    )
    subp_procar.add_argument("--orbital", help="Orbital of interest")
    subp_procar.add_argument("--occupation", help="Occupation of interest")
    subp_procar.add_argument("-e", "--energy", help="Energy of interest")
    subp_procar.add_argument("-s", "--spin", help="Spin channel of interest")
    subp_procar.add_argument(
        "-o", "--output", help="Output filename (either pickle file or queried results)"
    )
    subp_procar.add_argument(
        "-d",
        "--describe",
        action="store_true",
        help="Provides a brief description of the projected eigenvalues data",
    )
    subp_procar.add_argument(
        "--efermi", help="Reference Fermi Energy", type=float, default=0.0
    )
    subp_procar.add_argument("-S", "--structure", help="Structure file")

    # add argument group for file handling
    file_handling = subp_procar.add_argument_group("file handling")
    file_handling.add_argument(
        "-p",
        "--pickle",
        action="store_true",
        help="Write projected eigenvalues from a vasprun.xml file to a pickle file",
    )
    file_handling.add_argument(
        "--filter", help="Filter the projected eigenvalue data", action="store_true"
    )

    # add argument group for plotting
    plotting = subp_procar.add_argument_group("Band Plotting")
    plotting.add_argument("--plot", action="store_true")
    plotting.add_argument(
        "--kplot", help="Plot orbital variation of a single band", action="store_true"
    )
    plotting.add_argument(
        "--iplot",
        help="Plot compositional variation of a single band",
        action="store_true",
    )
    plotting.add_argument("--erange", nargs=2, type=float, help="Energy range to plot")
    plotting.add_argument("--irange", nargs=2, type=int, help="Index range to plot")
    plotting.add_argument("--labels", nargs="+", type=str, help="Labels for the plot")

    # add argument group for kpoint analysis and plotting
    kpoint_analysis = subp_procar.add_argument_group("kpoint analysis")
    kpoint_analysis.add_argument(
        "-a",
        "--analyze",
        help="Kpoint analysis of a specific kpoint and band",
        action="store_true",
    )


def wavecar(subparsers):
    subp_wavecar = subparsers.add_parser(
        "wavecar",
        help="Reads, analyses, and converts wavefunction information from WAVECAR and cube files",
    )

    # Argument group for standard specifications
    standard_specs = subp_wavecar.add_argument_group("Standard Specifications")
    standard_specs.add_argument(
        "-k", "--kpoints", help="Kpoint(s) of interest", type=int, nargs="+"
    )
    standard_specs.add_argument(
        "-b", "--bands", help="Band(s) of interest", type=int, nargs="+"
    )
    standard_specs.add_argument(
        "-s",
        "--spin",
        help="Spin channel(s) of interest. Do not specify if you want all spin and magnetization",
        type=str,
        default=None,
        choices=["0", "1", "up", "down"],
    )
    standard_specs.add_argument("--spinor", help="Spinor of interest", type=int)
    standard_specs.add_argument("-P", "--phase", help="Phase of interest", type=int)
    standard_specs.add_argument(
        "--shift", help="Shift value of periodic part of wavefunction", type=int
    )
    standard_specs.add_argument(
        "--scale", help="Scaling factor for PARCHG mesh density", type=int, default=2
    )
    standard_specs.add_argument("--vasp-type", help="VASP type", type=str, choices=['std', 'gam', 'ncl'], default=None)
    standard_specs.add_argument("--prec", help="Precision of the WAVECAR file", type=str, choices=['normal', 'accurate'], default='normal')

    # Argument group for functional choices
    functional_choices = subp_wavecar.add_argument_group("Functional Choices")
    functional_choices.add_argument(
        "-p",
        "--parchg",
        help="Generate a PARCHG file from a WAVECAR file",
        action="store_true",
    )
    functional_choices.add_argument(
        "-c",
        "--cube",
        help="Save WAVECAR partial charge density as a cube file",
        action="store_true",
    )
    functional_choices.add_argument(
        "-m",
        "--mesh",
        help="Extract wavefunction coefficients projected onto a 3D mesh",
        action="store_true",
    )
    functional_choices.add_argument(
        "-u",
        "--unk",
        help="Generate UNK files from a WAVECAR file",
        action="store_true",
    )

    info_choices = subp_wavecar.add_argument_group("Information Choices")
    info_choices.add_argument(
        "--nk", help="Print number of kpoints to stdout", action="store_true"
    )
    info_choices.add_argument(
        "--nb", help="Print number of bands to stdout", action="store_true"
    )
    info_choices.add_argument(
        "--efermi", help="Print Fermi energy to stdout", action="store_true"
    )
    info_choices.add_argument(
        "--occ", help="Print bands near the Fermi level to stdout", action="store_true"
    )

    subp_wavecar.add_argument("input", help="WAVECAR or cube file")
    subp_wavecar.add_argument("-S", "--structure", help="Structure file")
    subp_wavecar.add_argument("-o", "--output", help="Output filename", type=str)


def chgcar(subparsers):
    subp_chgcar = subparsers.add_parser(
        "chgcar",
        help="Reads, analyses, and converts charge density information from PARCHG and CHGCAR files",
    )
    subp_chgcar.add_argument("input", help="PARCHG or CHGCAR file(s)", nargs="+")
    subp_chgcar.add_argument(
        "-c", "--cube", help="Save CHGCAR or PARCHG as a cube file", action="store_true"
    )
    subp_chgcar.add_argument(
        "-s", "--sum", help="Add multiple PARCHG or CHGCAR files", action="store_true"
    )
    subp_chgcar.add_argument(
        "-d", "--diff", help="Subtract two PARCHG or CHGCAR files", action="store_true"
    )
    subp_chgcar.add_argument(
        "-o", "--output", help="Save a PARCHG or CHGCAR file", type=str
    )


def stm(subparsers):
    subp_stm = subparsers.add_parser(
        "stm", help="Reads, analyses, and plots STM data from CHGCAR or cube files"
    )
    subp_stm.add_argument("input", help="CHGCAR or cube file")
    subp_stm.add_argument("-H", "--height", help="Height of the slice", type=float)
    subp_stm.add_argument(
        "-D",
        "--dims",
        help="Repeat in x and y dimensions",
        type=int,
        nargs=2,
        default=[1, 1],
    )
    subp_stm.add_argument("-a", "--animate", help="Animate slices", action="store_true")
    subp_stm.add_argument(
        "-p",
        "--plot",
        help="Plot charge density slice at a certain height",
        action="store_true",
    )
    subp_stm.add_argument(
        "-t", "--title", help="Title of the plot", type=str, default="Charge Density"
    )
    subp_stm.add_argument("-o", "--output", help="Output file name", type=str)


def setup(subparsers):
    scripts = [
        adsorb,
        alchemy,
        analysis,
        band,
        chgcar,
        cohp,
        db,
        incar,
        kpoints,
        manage,
        poscar,
        procar,
        slab,
        stm,
        wavecar,
    ]
    for script in scripts:
        script(subparsers)
