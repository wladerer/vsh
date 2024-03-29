from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.core.structure import Molecule, Structure
from pymatgen.core.surface import Slab
from pymatgen.io.vasp.inputs import Poscar


def slab_from_structure(miller: list[int], structure: Structure) -> Slab:
    """
    Returns a pymatgen.core.surface.Slab from a pymatgen structure
    """
    import numpy as np

    # if miller is None, raise error
    if miller is None:
        raise ValueError("miller index is required")

    return Slab(
        lattice=structure.lattice,
        species=structure.species_and_occu,
        coords=structure.frac_coords,
        miller_index=miller,
        oriented_unit_cell=structure,
        shift=0,
        scale_factor=np.eye(3, dtype=int),
        site_properties=structure.site_properties,
    )


def structure_from_file(filename: str) -> Structure:
    """
    Creates a pymatgen structure from a file
    """
    structure = Structure.from_file(filename, sort=True, primitive=False)

    return structure


def adsorbate_from_file(filename: str) -> Molecule:
    """
    Creates a pymatgen molecule from a file
    """
    adsorbate = Molecule.from_file(filename)

    return adsorbate


def get_chemical_formula(structure: Structure) -> str:
    """
    Returns the chemical formula of a structure
    """
    return structure.composition.reduced_formula


def add_adsorbate_single(
    structure: Structure,
    adsorbate: Molecule,
    coverage: list[int] = [1, 1, 1],
    distance: float = 1.0,
    positions=("ontop", "bridge", "hollow"),
) -> list[Structure]:
    """
    Finds all adsorption sites on a structure and adsorbs the adsorbate at each site. Returns a list of adsorbed structures.
    """

    asf = AdsorbateSiteFinder(structure)
    ads_structs = asf.generate_adsorption_structures(
        adsorbate,
        repeat=coverage,
        find_args={"distance": distance, "positions": positions},
    )  # edit later

    return ads_structs


def add_adsorbate_on_both_surfaces(
    structure: Structure,
    adsorbate: Molecule,
    miller_plane: list[int],
    coverage: list[int] = [1, 1, 1],
    distance: float = 1.0,
    positions=("ontop", "bridge", "hollow"),
) -> list[Structure]:
    """
    Finds all adsorption sites on a structure and adsorbs the adsorbate at each site. Returns a list of adsorbed structures.
    """
    slab = slab_from_structure(miller=miller_plane, structure=structure)
    asf = AdsorbateSiteFinder(slab)
    ads_structs = asf.adsorb_both_surfaces(
        adsorbate,
        repeat=coverage,
        find_args={"distance": distance, "positions": positions},
    )  # edit later

    return ads_structs


def write_structure(structure, prefix: str = "", suffix: str = "") -> None:
    """
    Writes a structure to a file
    """
    # create Poscar object
    formula = get_chemical_formula(structure)
    poscar = Poscar(structure, comment="Generated by vsh")
    poscar.write_file(f"{prefix}_{formula}_{suffix}")


def create_adsorbed_structure(args):
    # get adsorption sites
    structure = structure_from_file(args.input)
    adsorbate = adsorbate_from_file(args.adsorbate)

    # if positions = 'all', then set positions to be positions=('ontop', 'bridge', 'hollow')
    if args.positions == "all":
        args.positions = ("ontop", "bridge", "hollow")

    if args.both:
        ads_structs = add_adsorbate_on_both_surfaces(
            structure,
            adsorbate,
            miller_plane=args.plane,
            coverage=args.coverage,
            distance=args.distance,
            positions=args.positions,
        )
    else:
        ads_structs = add_adsorbate_single(
            structure,
            adsorbate,
            coverage=args.coverage,
            distance=args.distance,
            positions=args.positions,
        )

    poscars = [Poscar(ads_struct, sort_structure=True) for ads_struct in ads_structs]

    return poscars


def run(args):
    # create adsorbed structures
    poscars = create_adsorbed_structure(args)

    if not args.output:
        for poscar in poscars:
            print(poscar.get_str())
    else:
        for i, poscar in enumerate(poscars):
            poscar.write_file(f"{args.output}_{i}.vasp")

    return None
