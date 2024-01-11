import pandas as pd
import pickle

def read_procar_with_pyprocar(procar_path: str, efermi: float = None, outcar_path: str = None):
    '''Reads PROCAR and possibly OUTCAR if fermi level is not given. Uses PyProcar Implementation'''
    from pyprocar.io.vasp import Procar
    from pyprocar.core import ElectronicBandStructure

    if not efermi and outcar_path:
        raise Exception('Fermi Energy or Outcar not supplied, cannot continue')

    if not efermi:
        from pymatgen.io.vasp import Outcar
        efermi = Outcar(outcar_path).efermi

    return Procar(procar_path, efermi=efermi)

# def dict_to_dataframe(projected_eigenvalues: dict) -> pd.DataFrame:
#     '''Creates a pandas dataframe from the projected eigenvalues dict'''

#     #spin
#     #kpoint
#     #band
#     #atom 
#     #orbital
        

#     return pd.DataFrame(formatted_values)


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



# data = projected_eigenvals_from_vasprun('/Users/wladerer/research/pt3sn/slabs/001/al8/sod/band/vasprun.xml')
# save_eigenvals(data, 'test.pkl')
from pymatgen.electronic_structure.core import Spin



data = projected_eigenvalues_from_pickle('test.pkl')


# Create an empty DataFrame
df = pd.DataFrame(columns=['Spin', 'Kpoint', 'Band', 'Ion'])

# Iterate over each value in data



# Print the resulting DataFrame
df = pd.DataFrame(columns=['Spin', 'Kpoint', 'Band', 'Ion'])

for spin, kpoints in data.items():
    for kpoint, bands in kpoints.items():
        for ions in bands:
            for values in ions.item():
                df = df.append({'Spin': spin, 'Kpoint': kpoint, 'Band': band, 'Ion': ion}, ignore_index=True)

print(df)


