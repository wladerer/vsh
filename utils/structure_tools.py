import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from ase.io import read

def xyz_to_dataframe(file: str):
    '''Reads an xyz file and returns a pandas dataframe.'''
    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line.split() for line in lines]
        lines = [line for line in lines if len(line) == 4]
        df = pd.DataFrame(lines, columns=['atom', 'x', 'y', 'z'])
        df[['x', 'y', 'z']] = df[['x', 'y', 'z']].astype(float)

        return df

def vasp_to_dataframe(file: str) -> pd.DataFrame:
    '''Reads a POSCAR or CONTCAR and returns a dataframe'''
    atoms = read(file)
    elements = atoms.get_chemical_symbols()
    positions = atoms.get_positions()

    lines = [ [element, position[0], position[1], position[2]] for element,position in zip(elements,positions) ]

    df = pd.DataFrame(lines, columns=['atom', 'x', 'y', 'z'])
    df[['x', 'y', 'z']] = df[['x', 'y', 'z']].astype(float)

    return df


def sort_df_by_height(df : pd.DataFrame):
    '''Sorts a dataframe by the z coordinate.'''
    df = df.sort_values(by=['z'], ascending=False)
    df = df.reset_index(drop=True)

    return df

def get_top_n_atoms(df: pd.DataFrame, n: int):
    '''Returns the top n atoms of a dataframe.'''
    return df.iloc[:n, :]


def vasp_to_distance_matrix(file: str, n: int = 12):
    '''Reads a POSCAR or CONTCAR and returns a distance matrix'''
    data = vasp_to_dataframe(file)
    data = sort_df_by_height(data)
    dist = distance_matrix(data.iloc[:n, 1:], data.iloc[:n, 1:])
    dist = pd.DataFrame(dist)
    atom_labels = data.iloc[:n, 0].values
    dist.index = atom_labels
    dist.columns = atom_labels

    return dist

def calculate_rdf(coordinates, bins=1000, r_max=15):
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


def plot_radial_distribution_function(input_files: list[str], labels: list[str], output_file: str = None):
    '''Plots the radial distribution function of a structure'''
    import plotly.graph_objects as go
    from pymatgen.core import Structure

    fig = go.Figure()

    for input_file, label in zip(input_files, labels):
        coords = Structure.from_file(input_file).cart_coords
        bin_centers, rdf = calculate_rdf(coords)

        # Add trace for each input file
        fig.add_trace(go.Scatter(x=bin_centers, y=rdf, mode='lines', name=label))

    fig.update_layout(
        title='Radial distribution function',
        xaxis_title='Distance (Å)',
        yaxis_title='RDF',
        template='plotly_white'
    )

    if not output_file:
        fig.show()
    else:
        fig.write_image(output_file)

### symmetry tool section

def get_symmetry_operations(file: str):
    '''Returns the symmetry operations of a POSCAR or CONTCAR file.'''
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    from pymatgen.core import Structure

    structure = Structure.from_file(file)
    sga = SpacegroupAnalyzer(structure)
    symmetry_operations = sga.get_symmetry_operations()

    return symmetry_operations


def plot_atomic_drift(initial_file: str, final_file: str, output_file: str = None):
    '''Plots the atomic drift between two structures'''
    from ase.io import read
    from ase.data.colors import jmol_colors, cpk_colors
    from ase.data import covalent_radii
    import numpy as np
    import plotly.graph_objects as go

    initial = read(initial_file)
    final = read(final_file)

    #atom types 
    atomic_numbers = initial.get_atomic_numbers()
    atom_types = initial.get_chemical_symbols()
    atomic_radii = [ covalent_radii[number] for number in atomic_numbers ]
    atomic_colors = [ jmol_colors[number] for number in atomic_numbers ]
    drift = final.get_positions() - initial.get_positions()

    fig = go.Figure()

    for i in range(len(initial)):
        atom = initial[i]
        x, y, z = atom.position
        dx, dy, dz = drift[i]
        r = atomic_radii[i]
        color = f"rgb({atomic_colors[i][0]}, {atomic_colors[i][1]}, {atomic_colors[i][2]})",
        fig.add_trace(go.Scatter3d(
            x=[x+dx, x],
            y=[y+dy, y],
            z=[z+dz, z],
            mode='lines+markers',
            marker=dict(
                size=18,
                color=color,
                line=dict(
                    color='DarkSlateGrey',
                    width=2
                )
            ),
            line=dict(
                color=color,
                width=2
            ),
            name=atom_types[i]
        ))


    fig.update_layout(
            title='Atomic drift',
            scene=dict(
                xaxis_title='x (Å)',
                yaxis_title='y (Å)',
                zaxis_title='z (Å)'
            )
        )

    
    #remove grid 
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False )


    if not output_file:
        fig.show()
    else:
        fig.write_image(output_file)

