from ase.io import read
import os
import numpy as np

def get_atoms(args):
    '''Creates ASE atoms object from a file'''

    atoms = read(args.input)
    
    return atoms

def sort_poscar(args):
    '''Sorts a POSCAR file'''
    from pymatgen.core import Structure
    from pymatgen.io.vasp.inputs import Poscar

    structure = Structure.from_file(args.input)
    poscar = Poscar(structure, sort_structure=True)
    
    if not args.output:
        print(poscar.get_str())
    else:
        poscar.write_file(f'{args.output}')

    return poscar


def boxed_molecule(args):
    '''Creates a boxed molecule from an input file'''
    from pymatgen.core import Structure, Molecule
    from pymatgen.io.vasp.inputs import Poscar

    #read the molecule
    box_molecule: Structure = Molecule.from_file(args.input).get_boxed_structure(a=args.vacuum, b=args.vacuum, c=args.vacuum, no_cross=args.no_cross)
    poscar = Poscar(box_molecule, sort_structure=True)

    if not args.output:
        print(poscar.get_str())
    else:
        poscar.write_file(f'{args.output}')


def convert_to_poscar(args):
    '''Converts a file to a POSCAR file'''
    from pymatgen.io.vasp.inputs import Poscar 

    structure = read(args.input)
    poscar = Poscar(structure, sort_structure=args.sort)

    if not args.output:
        print(poscar.get_str())    
    else:
        poscar.write_file(f'{args.output}')

    return poscar

def make_supercell(args):
    '''Make a supercell of a structure'''
    from pymatgen.io.vasp.inputs import Poscar
    from pymatgen.core import Structure
    from pymatgen.transformations.standard_transformations import SupercellTransformation
    
    structure = Structure.from_file(args.input)
    transformation = SupercellTransformation(args.super)
    supercell = transformation.apply_transformation(structure)
    
    poscar = Poscar(supercell, sort_structure=args.sort)
    
    if not args.output:
        print(poscar.get_str())
    else:
        poscar.write_file(f'{args.output}')
        
def list_selective_dynamics(args):
    '''Lists atoms and their selective dynamics'''
    import pandas as pd
    from pymatgen.io.vasp.inputs import Poscar
    poscar = Poscar.from_file(args.input)

    atoms = read(args.input).get_chemical_symbols()
    dynamics = poscar.selective_dynamics
    heights = poscar.structure.cart_coords[:, 2]

    if dynamics is None:
        dynamics = [[True, True, True]]*len(atoms)

    atom_tuples = [ (atom, index, sd, height) for atom, index, sd, height in zip(atoms, range(0, len(atoms)), dynamics, heights) ]
    #create a dataframe
    df = pd.DataFrame(atom_tuples, columns=['atom', 'index', 'selective_dynamics', 'height'])

    if not args.output:
        
        #print without index and print the whole dataframe
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df.to_string(index=False))

    else:
        df.to_csv(args.output, index=False)

def list_poscar(args):
    '''Lists the atoms by height file'''
    import pandas as pd
    atoms = read(args.input)

    heights = atoms.get_positions()[:, 2]
    atom_tuples = [ (atom, index, height) for atom, index, height in zip(atoms.get_chemical_symbols(), range(0, len(atoms)), heights) ]
    #create a dataframe
    df = pd.DataFrame(atom_tuples, columns=['atom', 'index', 'height'])
    
    #sort by height
    df = df.sort_values(by=['height'])
    df = df.reset_index(drop=True)
    
    
    if not args.output:
        
        #print without index and print the whole dataframe
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df.to_string(index=False))

    else:
        df.to_csv(args.output, index=False)


def calculate_rdf(coordinates, bins=1000, r_max=None):
    """
    Calculate the radial distribution function (RDF) from a set of XYZ coordinates.

    Parameters:
    - coordinates: numpy array of shape (n_particles, 3) representing XYZ coordinates.
    - bins: number of bins for histogram.
    - r_max: maximum distance to consider.

    Returns:
    - bin_centers: centers of the bins.
    - rdf: radial distribution function.
    """
    n_particles = len(coordinates)
    if r_max is None:
        r_max = np.max(np.linalg.norm(coordinates - coordinates[0], axis=1))

    # Calculate pairwise distances
    distances = np.sqrt(np.sum((coordinates[:, np.newaxis] - coordinates)**2, axis=-1))

    # Create histogram
    hist, bin_edges = np.histogram(distances, bins=bins, range=(0, r_max))

    # Calculate bin centers and RDF
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    rdf = hist / (4 * np.pi * bin_centers**2 * (r_max / bins))

    # Remove the first bin because it is always 0
    bin_centers = bin_centers[1:]
    rdf = rdf[1:]

    # Normalize RDF
    rdf /= np.sum(rdf)

    return bin_centers, rdf


def plot_radial_distribution_function(args):
    '''Plots the radial distribution function of a structure'''
    import plotly.graph_objects as go
    from pymatgen.core import Structure

    coords = Structure.from_file(args.input).cart_coords
    bin_centers, rdf = calculate_rdf(coords)

    # Plot RDF
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=bin_centers, y=rdf, mode='lines'))
    fig.update_layout(
        title='Radial distribution function',
        xaxis_title='Distance (Å)',
        yaxis_title='RDF',
        template='plotly_white'
    )

    if not args.output:
        fig.show()

    else:
        fig.write_image(args.output)


def run(args):
    functions = {
        "sort": sort_poscar,
        "convert": convert_to_poscar,
        "super": make_supercell,
        "list": list_poscar,
        "dynamics": list_selective_dynamics,
        "box": boxed_molecule,
        "rdf": plot_radial_distribution_function
    }
    
    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)