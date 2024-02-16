#!/usr/bin/env python3


"""Orthogonalization utilities were written by Dr. Yonghyuk Lee"""

import numpy as np
from ase import Atoms
from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.vasp.inputs import Poscar


def structure_from_file(filename: str) -> Structure:
    return Structure.from_file(filename)


def slab_from_structure(
    structure: Structure,
    miller_plane: list,
    zmin,
    vacuum: float,
    is_primitive: bool,
    center_slab: bool,
    in_unit_planes: bool,
    reorient_lattice: bool,
    reduce: bool = True,
) -> list[Structure]:
    slabgen = SlabGenerator(
        structure,
        miller_plane,
        zmin,
        vacuum,
        primitive=is_primitive,
        center_slab=center_slab,
        in_unit_planes=in_unit_planes,
        reorient_lattice=reorient_lattice,
        lll_reduce=reduce,
    )
    return slabgen.get_slabs()


def slab_to_poscar(slab: Structure) -> None:
    """Generates a pymatgen Poscar object from a slab"""
    poscar = Poscar(slab, sort_structure=True)
    return poscar


def generate_filename(structure: Structure, miller_plane: list, zmin) -> str:
    formula = structure.formula.replace(" ", "")
    return f"{formula}_slab_{miller_plane[0]}{miller_plane[1]}{miller_plane[2]}_{zmin}"


def freeze_slab(structure: Structure, min_z: float) -> Structure:
    """Freezes atoms below a certain threshold"""

    for site in structure.sites:
        if site.z < min_z:
            site.properties["selective_dynamics"] = [False, False, False]
        else:
            site.properties["selective_dynamics"] = [True, True, True]


def update_structure(
    traj,
    soap_info={
        "rcut": 5,
        "nmax": 8,
        "lmax": 4,
    },
):
    from dscribe.descriptors import SOAP
    from sklearn.preprocessing import normalize

    species = []
    if isinstance(traj, list):
        for t in traj:
            elements = np.unique(t.get_chemical_symbols())
            for e in elements:
                if e not in species:
                    species.append(e)
    elif isinstance(traj, Atoms):
        elements = np.unique(traj.get_chemical_symbols())
        for e in elements:
            if e not in species:
                species.append(e)

    soap = SOAP(
        species=species,
        periodic=True,
        r_cut=soap_info["rcut"],
        n_max=soap_info["nmax"],
        l_max=soap_info["lmax"],
    )

    if isinstance(traj, list):
        for s in traj:
            try:
                del s.arrays["SOAP"]
            except:
                pass
            s.set_array("SOAP", normalize(soap.create(s)))
    elif isinstance(traj, Atoms):
        traj.set_array("SOAP", normalize(soap.create(traj)))

    return traj


def quick_score(
    test_structure,
    training_structure,
):
    soap_test = test_structure.arrays["SOAP"]
    soap_train = training_structure.arrays["SOAP"]
    scores = np.dot(soap_train, soap_test.transpose()) ** 2
    score = np.min(np.max(scores, axis=0))
    v = 2 * (1 - score)
    if v < 10e-10:
        score = 0
    else:
        score = np.sqrt(v)
    return score


def orthogonalize_slab(
    file: str, alpha: float = None, beta: float = None, gamma: float = None
):
    """Orthogonalizes a structure"""
    from ase.io import read

    origin = read(file)
    atoms = read(file)

    cell = atoms.cell.standard_form()[0]
    atoms.set_cell(cell, scale_atoms=True)

    cell = atoms.cell.cellpar()

    if alpha:
        cell[3] = alpha
    if beta:
        cell[4] = beta
    if gamma:
        cell[5] = gamma

    atoms.set_cell(cell)
    atoms.wrap()

    origin = update_structure(origin)
    atoms = update_structure(atoms)

    return atoms


def convert_vacuum_to_angstroms(vacuum_ang: float, structure: Structure) -> float:
    """Converts a vacuum value to angstroms"""
    # this is necessary because the vacuum value is in units of the lattice vectors
    a, b, c = structure.lattice.abc

    vacuum_d = (vacuum_ang // c) + 2

    return vacuum_d


def gen_slabs(args):
    """Generate slabs using pymatgen slab generator"""

    if args.in_unit_planes is True:
        vacuum = convert_vacuum_to_angstroms(
            args.vacuum, structure_from_file(args.input)
        )
    else:
        vacuum = args.vacuum

    structure = structure_from_file(args.input)
    slabs = slab_from_structure(
        structure=structure,
        miller_plane=args.miller_plane,
        zmin=float(args.thickness),
        vacuum=vacuum,
        is_primitive=args.primitive,
        center_slab=args.center_slab,
        in_unit_planes=args.in_unit_planes,
        reorient_lattice=args.reorient_lattice,
        reduce=not (
            args.no_reduce
        ),  # this is a bit confusing, but it is to maintain simplified default behavior
    )

    if args.freeze:
        for slab in slabs:
            freeze_slab(slab, args.freeze)

    poscars = [slab_to_poscar(slab) for slab in slabs]

    if not args.output:
        for poscar in poscars:
            print(poscar.get_str())
    else:
        for i, poscar in enumerate(poscars):
            poscar.write_file(f"{args.output}_{i}.vasp")


def orthogonalize(args):
    """Orthogonalize a slab"""
    from ase.io import read

    orginal_atoms = read(args.input)
    orthogonalized_atoms = orthogonalize_slab(
        args.input, args.alpha, args.beta, args.gamma
    )

    # convert to pymatgen structure
    orthogonalized_structure = AseAtomsAdaptor.get_structure(orthogonalized_atoms)
    poscar = Poscar(orthogonalized_structure, sort_structure=True)

    if args.verbose:
        orginal_atoms = update_structure(orginal_atoms)
        orthogonalized_atoms = update_structure(orthogonalized_atoms)
        print(f"Similarity score: {quick_score(orginal_atoms, orthogonalized_atoms)}")

    if args.freeze:
        freeze_slab(orthogonalized_structure, args.freeze)

    if not args.output:
        print(poscar.get_str())
    else:
        poscar.write_file(f"{args.output}")


def run(args):
    if args.orthogonalize:
        orthogonalize(args)

    else:
        gen_slabs(args)
