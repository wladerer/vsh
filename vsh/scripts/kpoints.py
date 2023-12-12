from ase.io import read, write

two_d_kpath_template = """Two dimensional Kpath 
   {{kpath}}
Line-Mode
Reciprocal
   0.5000000000   0.0000000000   0.0000000000     M
   0.3333333333   0.3333333333   0.0000000000     K

   0.3333333333   0.3333333333   0.0000000000     K
   0.0000000000   0.0000000000   0.0000000000     GAMMA

   0.0000000000   0.0000000000   0.0000000000     GAMMA
   0.5000000000   0.0000000000   0.0000000000     M

"""

def get_atoms(args):
    '''Creates ASE atoms object from a file'''

    atoms = read(args.input)
    
    return atoms

def write_kpoints(args):
    '''Writes a KPOINTS file'''
    from pymatgen.io.vasp.inputs import Kpoints 

    kpoints = Kpoints.gamma_automatic(kpts=args.mesh)

    if not args.output:
        print(kpoints)

    else:
        kpoints.write_file(f'{args.output}')

    return kpoints


def write_path(args):
    '''
    Makes a linemode Kpoints object from a structure
    '''
    from pymatgen.core import Structure
    from pymatgen.io.vasp.inputs import Kpoints 
    from pymatgen.symmetry.bandstructure import HighSymmKpath

    structure = Structure.from_file(args.input)
    kpath = HighSymmKpath(structure)
    
    #make sure path is an int
    if args.path:
        args.path = int(args.path)
        
    kpoints = Kpoints.automatic_linemode(args.path, kpath)
    
    if not args.output:
        print(kpoints)
    else:
        kpoints.write_file(f'{args.output}')

    return kpoints

def write_plane(args) -> str:
    '''Creates a 2D kpath from a jinja 2 template'''
    from jinja2 import Template
    template = Template(two_d_kpath_template)
    kplane = template.render(kpath=args.plane)
    
    if not args.output:
        print(kplane)
    else:
        with open(args.output, "w") as f:
            f.write(kplane)
            
    return kplane

def run(args):
    functions = {
        "mesh": write_kpoints,
        "path": write_path,
        "plane": write_plane
    }
    
    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)