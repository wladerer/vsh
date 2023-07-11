import argparse
from ase.io import read
from ase.calculators.vasp import Vasp
import sys

def yaml_to_dict(filename):
    '''Convert yaml file to dictionary'''
    import yaml
    with open(filename, 'r') as f:
        return yaml.load(f)
    
def create_input_dicts(base_incar: dict, step: float, number: int, tag: str):
    '''Create input dictionaries for each variation'''
    input_dicts = []
    for i in range(number):
        incar = base_incar.copy()
        incar[tag] = i * step
        input_dicts.append(incar)

    return input_dicts

def create_dicts_from_custom(base_incar: dict, custom: list, tag: str):
    '''Create input dictionaries from custom steps'''
    input_dicts = []
    for i, step in enumerate(custom):
        incar = base_incar.copy()
        incar[tag] = step
        input_dicts.append(incar)

    return input_dicts

def create_variations():
    parser = argparse.ArgumentParser(description='Create variations of a vasp job')

    parser.add_argument('-f', '--file', type=str, help='Structure file')
    parser.add_argument('-i', '--incar', type=str, help='Base incar.yaml file')
    parser.add_argument('-c', '--custom', nargs='+', help='Custom steps. Tag must be specified with -t or --tag')
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of variations')
    parser.add_argument('-s', '--step', type=float, help='Step size')
    parser.add_argument('-t', '--tag', type=str, default='var', help='Tag for variation files')
    parser.add_argument('-d', '--basedir', type=str, default='step', help='Base directory')
    parser.add_argument('-k, --kpoints', type=int, nargs=3, help='Kpoints', default=[1, 1, 1])
    args = parser.parse_args()
    atoms = read(args.file)

    #tags
    base_incar: dict = yaml_to_dict(args.incar)

    #remove specified tag from base_incar if it exists
    if args.tag in base_incar:
        del base_incar[args.tag]

    #throw error if yaml file is not specified
    if not args.incar:
        raise ValueError('Incar file must be specified.')

    #throw error if step, number, and tag are not specified
    if not args.step or not args.number or not args.tag or not args.custom:
        raise ValueError('Step, number, and tag must be specified.')
    
    #create variations
    if args.step and args.number:
        input_dicts = create_input_dicts(base_incar, args.step, args.number, args.tag)
    elif args.custom:
        input_dicts = create_dicts_from_custom(base_incar, args.custom, args.tag)

    #add kpoints to input_dicts
    for incar in input_dicts:
        incar['kpts'] = args.kpoints

    #write variations to files
    for i, incar in enumerate(input_dicts):
        dir_name = f'{args.basedir}_{i}'
        calc = Vasp(atoms=atoms, **incar)
        

if __name__ == '__main__':
    create_variations()
    
