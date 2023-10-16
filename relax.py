from ase.io import read, write
from ase.calculators.vasp import Vasp
import argparse

low_slab_options = {'encut': 400, 'ibrion': 2, 'nsw': 100, 'isif': 2, 'ediff': 0.5e-5, 'ediffg': -0.01, 'lwave': False}
low_bulk_options = {'encut': 400, 'ibrion': 2, 'nsw': 100, 'isif': 3, 'ediff': 0.5e-5, 'ediffg': -0.01, 'lwave': False}
med_slab_options = {'encut': 520, 'ibrion': 2, 'nsw': 100, 'isif': 2, 'ediff': 1.0e-5, 'ediffg': -0.01, 'lwave': False}
med_bulk_options = {'encut': 520, 'ibrion': 2, 'nsw': 100, 'isif': 3, 'ediff': 1.0e-5, 'ediffg': -0.01, 'lwave': False}

med_single_point = {'encut': 520, 'ibrion': 2, 'nsw': 0, 'isif': 2, 'ediff': 1.0e-5, 'ediffg': -0.01, 'lwave': False}

bader = {'lcharg': True, 'laechg': True}
soc_options = {'lsorbit': True, 'lwave': False, 'lcharg': False}

def create_vasp_inputs():
    '''Creats a VASP job directory for the given structure and parameters.'''
    parser = argparse.ArgumentParser(description='Create VASP input files for a given structure.')
    parser.add_argument('-f', '--file', type=str, help='Structure file', required=True)
    parser.add_argument('-a', '--acurracy', type=str, choices=['low', 'med', 'high'], help='Accuracy of the calculation')
    parser.add_argument('-t', '--type', type=str, choices=['slab', 'bulk', 'single_point'], help='Type of calculation')
    parser.add_argument('-s', '--soc', action='store_true', help='Include spin-orbit coupling')
    parser.add_argument('-b', '--bader', action='store_true', help='Include Bader charge analysis')
    parser.add_argument('-k', '--kpoints', type=int, nargs=3, help='K-point mesh', default=[7, 7, 7])
    parser.add_argument('-x', '--xc', type=str, choices=['pbe', 'pbesol'], help='Exchange-correlation functional', default='pbe')  
    args = parser.parse_args()

    atoms = read(args.file)

    if args.acurracy == 'low':
        if args.type == 'slab':
            options = low_slab_options
        elif args.type == 'bulk':
            options = low_bulk_options
        elif args.type == 'single_point':
            options = med_single_point

    elif args.acurracy == 'med':
        if args.type == 'slab':
            options = med_slab_options
        elif args.type == 'bulk':
            options = med_bulk_options
        elif args.type == 'single_point':
            options = med_single_point

    elif args.acurracy == 'high':
        if args.type == 'slab':
            options = med_slab_options
        elif args.type == 'bulk':
            options = med_bulk_options
        elif args.type == 'single_point':
            options = med_single_point

    if args.soc:
        options.update(soc_options)

    if args.bader:
        options.update(bader)

    if args.kpoints:
        options.update({'kpts': args.kpoints})

    if args.xc:
        options.update({'xc': args.xc})

    calc = Vasp(**options)
    atoms.calc = calc
    calc.write_input(atoms) 








