import pandas as pd

def get_fermi_bands(dataframe: pd.DataFrame, efermi: float, tolernace: float = 0.1):
    """Gets the bands that are within the tolerance of the fermi level"""
    dataframe = dataframe[dataframe["Energy"] >= efermi - tolernace]
    dataframe = dataframe[dataframe["Energy"] <= efermi + tolernace]
    bands = dataframe["Band"].unique()
    
    return bands

def update_kpoint_coordinates(dataframe: pd.DataFrame, kpoint_coordinates: dict):
    '''Updates the kpoint coordinates in the dataframe'''
    dataframe['Kpoint'] = dataframe['Kpoint'].map(kpoint_coordinates)
    return dataframe

def get_fermi_surface_points(dataframe: pd.DataFrame, bands: list[int]):
    '''Gets the kpoints that are on the fermi surface'''
    dataframe = dataframe[dataframe["Band"].isin(bands)]
    kpoints = dataframe["Kpoint"].unique()
    return kpoints

def create_kpoint_mesh(dataframe: pd.DataFrame, kpoints: list[int]):
    '''Creates a mesh grid of kpoints to plot the fermi surface'''
    kpoint_coordinates = dict(zip(kpoints, range(len(kpoints))))
    dataframe = update_kpoint_coordinates(dataframe, kpoint_coordinates)
    nkpoints = dataframe['Kpoint'].nunique()
    nbands = dataframe['Band'].nunique()
    kpoint_mesh = np.zeros((nkpoints, nbands))
    for kpoint in kpoints:
        kpoint_data = dataframe[dataframe['Kpoint'] == kpoint]
        kpoint_mesh[kpoint, kpoint_data['Band']] = kpoint_data['Energy']
    return kpoint_mesh