#!/usr/bin/env python3

import argparse
from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator
from pymatgen.io.vasp.inputs import Poscar 

def structure_from_file(filename: str) -> Structure:
    return Structure.from_file(filename)


def slab_from_structure(structure: Structure, miller_plane: list, zmin, vacuum: float, is_primitive: bool, center_slab: bool, in_unit_planes: bool) -> list[Structure]:
    slabgen = SlabGenerator(structure, miller_plane, zmin, vacuum, primitive=is_primitive, center_slab=center_slab, in_unit_planes=in_unit_planes)
    return slabgen.get_slabs()

def write_slab_to_poscar(slab: Structure, filename: str) -> None:
    poscar = Poscar(slab, sort_structure=True)
    poscar.write_file(filename)

def generate_filename(structure: Structure, miller_plane: list, zmin) -> str:
    formula = structure.formula.replace(' ', '')
    return f'{formula}_slab_{miller_plane[0]}{miller_plane[1]}{miller_plane[2]}_{zmin}'

def freeze_slab(structure: Structure, min_z: float) -> Structure:
    '''Freezes atoms below a certain threshold'''

    for site in structure.sites:
        if site.z < min_z:
            site.properties['selective_dynamics'] = [False, False, False]
        else:
            site.properties['selective_dynamics'] = [True, True, True]
    


def create_slabs():
    parser = argparse.ArgumentParser(description='Create slabs using pymatgen')


    parser.add_argument('-f', '--file', type=str, help='Structure file', required=True)
    parser.add_argument('-m', '--miller-plane', type=int, nargs=3, default=[0, 0, 1], help='Miller plane')
    parser.add_argument('-o', '--output', type=str, help='Output file basename')
    parser.add_argument('--sort', help='Sort atoms')
    parser.add_argument('-v', '--vacuum', type=float, default=15.0, help='Vacuum size')
    parser.add_argument('-s', '--symmetric', type=bool, default=True, help='Ensure that the faces of the slab are symmetric')
    parser.add_argument('--zmin', default=15.0, help='Minimum slab thickness in Angstrom or multiples of miller plane spacing')
    parser.add_argument('--primitive', default=False, help='Create primitive cell')
    parser.add_argument('-c', '--center-slab', default=False, help='Center the slab')
    parser.add_argument('-u', '--in-unit-planes', default=False, type=bool, help='Specify zmin in multiples of miller plane spacing')
    parser.add_argument('--freeze', default=5, type=float, help='Freeze the bottom layer of the slab')

    args = parser.parse_args()

    structure = structure_from_file(args.file)
    slabs = slab_from_structure(structure, args.miller_plane, args.zmin, args.vacuum, args.primitive, args.center_slab, args.in_unit_planes)
    
    if args.freeze:
        for slab in slabs:
            freeze_slab(slab, args.freeze)
    
    for i, slab in enumerate(slabs):
        write_slab_to_poscar(slab, f'{generate_filename(structure, args.miller_plane, args.zmin)}_{i}.vasp')



if __name__ == '__main__':
    create_slabs()


    
    
