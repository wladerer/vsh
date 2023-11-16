#!/usr/bin/env python3

import argparse
from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator
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
) -> list[Structure]:
    slabgen = SlabGenerator(
        structure,
        miller_plane,
        zmin,
        vacuum,
        primitive=is_primitive,
        center_slab=center_slab,
        in_unit_planes=in_unit_planes,
    )
    return slabgen.get_slabs()


def write_slab_to_poscar(slab: Structure, filename: str) -> None:
    poscar = Poscar(slab, sort_structure=True)
    poscar.write_file(filename, direct=False)


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


def run(args):

    # check if in unit planes was selected, if so, adjust the vacuum to 3
    if args.in_unit_planes:
        args.vacuum = 3

    structure = structure_from_file(args.input)
    slabs = slab_from_structure(
        structure=structure,
        miller_plane=args.miller_plane,
        zmin=float(args.thickness),
        vacuum=args.vacuum,
        is_primitive=args.primitive,
        center_slab=args.center_slab,
        in_unit_planes=args.in_unit_planes,
    )

    if args.freeze:
        for slab in slabs:
            freeze_slab(slab, args.freeze)

    for i, slab in enumerate(slabs):
        write_slab_to_poscar(
            slab,
            f"{generate_filename(structure, args.miller_plane, args.thickness)}_{i}.vasp",
        )


