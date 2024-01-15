import pandas as pd
import numpy as np
import pickle
import itertools

orbital_dict = {'s': 0, 'p_y': 1, 'p_z': 2, 'p_x': 3, 'd_xy': 4, 'd_yz': 5, 'd_z2': 6, 'd_xz': 7, 'd_x2-y2': 8, 'f_y(3x2 -y2)': 9, 'f_xyz': 10, 'f_yz2':11, 'f_z3':12, 'f_xz2':13, 'f_z(x2 -y2)':14, 'f_x(x2 -3y2)':15}
orbital_dict = {value: key for key, value in orbital_dict.items()} #this is so stupid, i'm sorry

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

def eigenvalues_from_vasprun(file: str) -> pd.DataFrame:
    '''Gets eigenvalues and fermi energy from vasprun.xml file'''
    from pymatgen.io.vasp import Vasprun
    
    vasprun = Vasprun(filename=file, parse_potcar_file=False, parse_projected_eigen=False, parse_dos=False, parse_eigen=True)
    eigenvalues = vasprun.eigenvalues
    
    eigenvalues_list = [spin for spin in eigenvalues.values()]
    
    #create a dataframe with the kpoints, bands and eigenvalues
    value_dictionaries = []
    for spin_index, spin in enumerate(eigenvalues_list):
        nkpoints, nbands, _ = np.shape(spin)
        all_entries = list(itertools.product(*[range(nkpoints), range(nbands)]))
        for entry in all_entries:
            kpoint_index, band_index = entry
            energy = spin[kpoint_index][band_index][0]
            occupation = spin[kpoint_index][band_index][1]
            value_dict = dict(zip(['Spin', 'Kpoint', 'Band', 'Energy', 'Occupation'], [spin_index, kpoint_index, band_index, energy, occupation]))
            value_dictionaries.append(value_dict)
    
    df = pd.DataFrame(value_dictionaries)
    
    return df


def projected_eigenvals_from_vasprun(file: str) -> pd.DataFrame:
    from pymatgen.io.vasp import Vasprun
    '''Creates a band structure object from vasprun.xml file'''
    #format is [spin][kpoint index][band index][atom index][orbital_index]. The kpoint, band and atom indices are 0-based (unlike the 1-based indexing in VASP).
    vasprun = Vasprun(filename=file, parse_potcar_file=False, parse_projected_eigen=True)
    projected_values = dict_to_dataframe(vasprun.projected_eigenvalues)
    
    return projected_values

def merge_eigenvalues(eigenvalues: pd.DataFrame, projected_eigenvalues: pd.DataFrame) -> pd.DataFrame:
    '''Merges eigenvalues and projected eigenvalues'''
    merged = pd.merge(eigenvalues, projected_eigenvalues, on=['Spin', 'Kpoint', 'Band'])
    return merged


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

def load_dataframe_from_file(file: str):
    # load in the data, check if it is either xml or pkl
    if file.endswith('.xml'):
        projected_eigenvals = projected_eigenvals_from_vasprun(file)
        eigenvals = eigenvalues_from_vasprun(file)
        data = merge_eigenvalues(eigenvals, projected_eigenvals)

    elif file.endswith('.pkl'):
        data = projected_eigenvalues_from_pickle(file)
    else:
        raise Exception("Unrecognized file extension. Please provide either an XML or a pickle file.")

    return data


def filter_bands_by_energy(dataframe: pd.DataFrame, emin: float, emax: float):
    '''Filter bands by energy'''
    filtered_dataframe = dataframe[(dataframe['Energy'] >= emin) & (dataframe['Energy'] <= emax)]
    nkpoints = filtered_dataframe['Kpoint'].nunique()

    #keep only bands that have a complete set of kpoints
    filtered_dataframe = filtered_dataframe.groupby('Band').filter(lambda x: x['Kpoint'].nunique() == nkpoints)

    return filtered_dataframe


def filter_bands_by_index(dataframe: pd.DataFrame, index_min: int, index_max: int):
    '''Filter bands by index'''
    filtered_dataframe = dataframe[(dataframe['Band'] >= index_min) & (dataframe['Band'] <= index_max)]
    return filtered_dataframe

def get_kpoint_data(file: str, kpoint: int, band: int):
    '''Summarizes the data for a specific kpoint'''
    dataframe = load_dataframe_from_file(file)

    kpoint_data = dataframe[(dataframe['Kpoint'] == int(kpoint)) & (dataframe['Band'] == int(band))]
    kpoint_data = kpoint_data.groupby(['Spin', 'Kpoint', 'Band', 'Orbital']).sum().reset_index()
    
    #convert "value" to "percent" wrt to orbitals
    kpoint_data['Percent'] = kpoint_data['Value'] / kpoint_data['Value'].sum() * 100

    return kpoint_data

def get_kpoint_orbital_variation(file: str, band: int):
    '''Plots the orbital variation within a band'''
    dataframe = load_dataframe_from_file(file)
    dataframe = dataframe[dataframe['Band'] == int(band)]
    dataframe = dataframe.groupby(['Spin', 'Kpoint', 'Band', 'Orbital']).sum().reset_index()
    
    #iterate over each Kpoint
    for kpoint in dataframe['Kpoint'].unique():
        kpoint_data = dataframe[dataframe['Kpoint'] == int(kpoint)]
        kpoint_data['Percent'] = kpoint_data['Value'] / kpoint_data['Value'].sum() * 100

        #update dataframe with percent values
        dataframe.loc[dataframe['Kpoint'] == int(kpoint), 'Percent'] = kpoint_data['Percent']
    
    return dataframe


def plot_kpoint_orbital_variation(args):
    #plot each orbital percentage against kpoints
    dataframe = load_dataframe_from_file(args.input)
    dataframe = get_kpoint_orbital_variation(args.input, args.band)
    import plotly.graph_objects as go
    fig = go.Figure()
    for orbital in dataframe['Orbital'].unique():
        orbital_data = dataframe[dataframe['Orbital'] == orbital]
        fig.add_trace(go.Scatter(x=orbital_data['Kpoint'], y=orbital_data['Percent'], mode='lines', name=f'{orbital_dict[orbital]}'))

    #update legend according to orbital_dict 

    fig.update_layout(title=f'Band {args.band} Orbital Variation', xaxis_title='Kpoint', yaxis_title='Orbital Contribution (%)')

    # add axis tick labels if --labels is given
    if args.labels:
        nkpoints = dataframe['Kpoint'].nunique()
        #evenly space the labels across the x-axis
        xtickvals = np.linspace(0, nkpoints, len(args.labels))
        xticktext = args.labels
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=xtickvals, ticktext=xticktext))
        



    fig.show()



def analyze_kpoint(args):
    '''Summarizes the data for a specific kpoint'''
    dataframe = load_dataframe_from_file(args.input)
    kpoint = args.kpoint
    band = args.band

    kpoint_data = get_kpoint_data(args.input, kpoint, band)

    print(f"Kpoint: {kpoint}")
    print(f"Band: {band}")
    #print the percent of each orbital
    for orbital in range(kpoint_data['Orbital'].nunique()):
        orbital_data = kpoint_data[kpoint_data['Orbital'] == orbital]
        percent = orbital_data['Percent'].iloc[0]
        print(f"Orbital {orbital}: {percent:.3f}%")



def plot_bands(args):
    import plotly.graph_objects as go

    data = load_dataframe_from_file(args.input)
    data = data[['Band', 'Kpoint', 'Energy']]
    data['Energy'] = data['Energy'] - args.efermi

    bands = data['Band'].unique()

    #filter bands by energy or index if irange or erange is given
    if args.irange:
        index_min, index_max = args.irange
        data = filter_bands_by_index(data, index_min, index_max)
        bands = data['Band'].unique()

    if args.erange:
        emin, emax = args.erange
        data = filter_bands_by_energy(data, emin, emax)
        bands = data['Band'].unique()

    fig = go.Figure()
    for band in bands:
        band_data = data[data['Band'] == band]
        kpoints = band_data['Kpoint']
        energies = band_data['Energy']
        fig.add_trace(go.Scatter(x=kpoints, y=energies, mode='lines', name=f'Band {band}'))



    fig.update_layout(title='Band Structure', xaxis_title='Kpoint', yaxis_title='Energy (eV)')
    fig.show()

def run_query(args):

    data = load_dataframe_from_file(args.input)

    query_dict = {
    'Spin': args.spin if args.spin is not None else None,
    'Kpoint': int(args.kpoint) if args.kpoint is not None else None, 
    'Band': int(args.band) if args.band is not None else None,
    'Ion': int(args.ion) if args.ion is not None else None,
    'Orbital': args.orbital if args.orbital is not None else None,
    'Occupation': args.occupation if args.occupation is not None else None,
    'Energy': args.energy if args.energy is not None else None
    }
    
    if args.efermi:
        data['Energy'] = data['Energy'] - args.efermi

    result = query_data(data, query_dict)

    if not args.output:
        print(result)
    else:
        result.to_csv(args.output, index=False)
        
def describe_procar(args):
    '''Briefly describes the PROCAR file'''
    dataframe = load_dataframe_from_file(args.input)
    unique_spins = dataframe['Spin'].nunique()
    unique_kpoints = dataframe['Kpoint'].nunique()
    unique_bands = dataframe['Band'].nunique()
    unique_ions = dataframe['Ion'].nunique()
    unique_orbitals = dataframe['Orbital'].nunique()

    print(f"Number of unique Spins: {unique_spins}")
    print(f"Number of unique Kpoints: {unique_kpoints}")
    print(f"Number of unique Bands: {unique_bands}")
    print(f"Number of unique Ions: {unique_ions}")
    print(f"Number of unique Orbitals: {unique_orbitals}")

    return None

def pickle_procar(args):
    if args.input.endswith('.pkl'):
        raise Exception('Cannot pickle a pickle')

    projected_eigenvals = projected_eigenvals_from_vasprun(args.input)
    eigenvals = eigenvalues_from_vasprun(args.input)
    dataframe = merge_eigenvalues(eigenvals, projected_eigenvals)


    if args.output:
        save_eigenvals(dataframe, args.output)
    else:
        print(dataframe.describe())

def run(args):

    functions = {
        "pickle": pickle_procar,
        "describe": describe_procar,
        "plot": plot_bands,
        "kplot": plot_kpoint_orbital_variation,
        "analyze": analyze_kpoint
    }
    
    selected = False
    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)
            selected = True
    
    if not selected:
        run_query(args)


        
    








                

                




