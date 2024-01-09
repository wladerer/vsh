import pandas as pd
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


