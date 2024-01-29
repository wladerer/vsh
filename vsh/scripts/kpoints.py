from ase.io import read, write
import numpy as np

two_d_kpath_template = """Two dimensional Kpath 
   {{ kpath }}
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

    if args.mesh_type == "monkhorst":

        kpoints = Kpoints.monkhorst_automatic(kpts=args.mesh)

    elif args.mesh_type == "gamma":

        kpoints = Kpoints.gamma_automatic(kpts=args.mesh)

    elif args.mesh_type == "automatic":

        if not args.input:
            raise ValueError("No input structure file provided. Automatic Density requires structure")
        kpoints = Kpoints.automatic_density(args.input, args.mesh)


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

    if not args.input:
        raise ValueError("No input structure file provided")
    
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

def hydbrid_mesh(step: float = 0.1, weight: int = 0):
    '''Updates KPOINT file for hybrid calculations'''
    

    #create a uniform grid of floats between 0 and 0.5 with a user defined step size (default 0.1)
    kpoints = np.arange(0, 0.5, step)
    grid = np.meshgrid(kpoints, kpoints, kpoints)
    grid = np.array(grid)
    grid = grid.reshape(3, -1)
    grid = grid.T

    #remove duplicate points
    grid = np.unique(grid, axis=0)

    return grid

def hybrid_mesh_to_string(grid: np.array, step: float = 0.1, weight: int = 0):
    '''Converts a hybrid mesh to a string for a KPOINTS file'''

    #convert the grid to a string
    grid_string = ''
    for point in grid:
        grid_string += f'{point[0]:.1f} {point[1]:.1f} {point[2]:.1f} {weight}\n'

    return grid_string

def append_hybrid_mesh(args):
    '''Adds a uniform mesh to a KPOINTS file'''

    with open(args.input, 'r') as f:
        lines = f.readlines()
        lines = [ line.strip() for line in lines ]
        grid_string = hybrid_mesh_to_string(hydbrid_mesh(step=args.step, weight=args.weight))
        lines.append(grid_string)
        lines = '\n'.join(lines)

    if not args.output:
        print(lines)
    else:
        with open(args.output, 'w') as f:
            f.write(lines)
    
    return None


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