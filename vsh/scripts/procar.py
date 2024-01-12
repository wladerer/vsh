import pandas as pd
import numpy as np
import pickle
import itertools

def read_procar_with_pyprocar(procar_path: str, efermi: float = None, outcar_path: str = None):
    '''Reads PROCAR and possibly OUTCAR if fermi level is not given. Uses PyProcar Implementation'''
    from pyprocar.io.vasp import Procar

    if not efermi and outcar_path:
        raise Exception('Fermi Energy or Outcar not supplied, cannot continue')

    if not efermi:
        from pymatgen.io.vasp import Outcar
        efermi = Outcar(outcar_path).efermi

    return Procar(procar_path, efermi=efermi)

def dict_to_dataframe(projected_eigenvalues: dict) -> pd.DataFrame:
    '''Creates a pandas dataframe from the projected eigenvalues dict'''

    columns = ['Spin', 'Kpoint', 'Band', 'Ion', 'Orbital', 'Value']
    data = projected_eigenvalues
    # Get all possible entries using itertools
    value_dictionaries = []
    for spin_index,spin in enumerate(data.values()):
        nkpoints, nbands, nions, norbitals = np.shape(spin)
        all_entries = list(itertools.product(*[range(nkpoints), range(nbands), range(nions), range(norbitals)]))
        for entry in all_entries:
            kpoint_index, band_index, ion_index, orbital_index = entry
            value = spin[kpoint_index][band_index][ion_index][orbital_index]
            value_dict = dict(zip(columns, [spin_index, kpoint_index, band_index, ion_index, orbital_index, value]))
            value_dictionaries.append(value_dict)

    df = pd.DataFrame(value_dictionaries)

    return df


def projected_eigenvals_from_vasprun(file: str) -> pd.DataFrame:
    from pymatgen.io.vasp import Vasprun
    '''Creates a band structure object from vasprun.xml file'''
    #format is [spin][kpoint index][band index][atom index][orbital_index]. The kpoint, band and atom indices are 0-based (unlike the 1-based indexing in VASP).
    vasprun = Vasprun(filename=file, parse_potcar_file=False, parse_projected_eigen=True)
    projected_values = vasprun.projected_eigenvalues

    return projected_values

def projected_eigenvalues_from_pickle(file: str) -> pd.DataFrame:
    '''Loads eigenvalues from pickle file'''
    
    with open(file, 'rb') as file:
        loaded_dict = pickle.load(file)
    
    return loaded_dict

def save_eigenvals(projected_eigenvalues: pd.DataFrame, filename: str) -> None:
    '''Pickles eigenvalue object'''
     
    with open(filename, 'wb') as file:
        pickle.dump(projected_eigenvalues, file)

    return None

def parse_query_input(query: dict):
    '''Formats query to be compatible with Pandas'''

    query_dict = {key: value for key, value in query.items() if value is not None}
    query_string = ' and '.join([f'{k} == {v}' for k, v in query_dict.items()])

    return query_string


def query_data(data: pd.DataFrame, query_dict: dict):
    '''Allows querying the data from the command line'''
    query = parse_query_input(query_dict)

    result = data.query(query)
    return result

def query(args):
    # load in the data, check if it is either xml or pkl
    if args.input.endswith('.xml'):
        data = projected_eigenvals_from_vasprun(args.input)
    elif args.input.endswith('.pkl'):
        data = projected_eigenvalues_from_pickle(args.input)
    else:
        print("Unrecognized file extension. Please provide either an XML or a pickle file.")

    query_dict = {
    'Spin': args.spin if args.spin is not None else None,
    'Kpoint': int(args.kpoint) if args.kpoint is not None else None, 
    'Band': int(args.band) if args.band is not None else None,
    'Ion': int(args.ion) if args.ion is not None else None,
    'Orbital': args.orbital if args.orbital is not None else None
    }
    
    result = query_data(data, query_dict)

    if not args.output:
        print(result)
    else:
        result.to_csv(args.output, index=False)


def run(args):

    if args.pickle:
       df = projected_eigenvals_from_vasprun(args.input) 
       if not args.output:
           raise Exception('Output filename not provided')
       else:
        save_eigenvals(df, args.output)

    else:
        query(args)

        
    








                

                




