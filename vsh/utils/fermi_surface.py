import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pymatgen.io.vasp.outputs import Vasprun


def projected_eigenvalues_from_pickle(file: str) -> pd.DataFrame:
    """Loads eigenvalues from pickle file"""
    with open(file, "rb") as file:
        loaded_dict = pickle.load(file)
    return loaded_dict


def kpoints_coordinates_from_vasprun(
    vasprun: Vasprun,
) -> list[list[float, float, float]]:
    """Gets the kpoints from a vasprun file"""
    kpoints: list[list[float, float, float]] = vasprun.actual_kpoints
    return kpoints


def get_fermi_band_indices(
    dataframe: pd.DataFrame, efermi: float, tolernace: float = 0.1
) -> list[int]:
    """Gets the bands that are within the tolerance of the fermi level"""
    dataframe = dataframe[dataframe["Energy"] >= efermi - tolernace]
    dataframe = dataframe[dataframe["Energy"] <= efermi + tolernace]
    bands = dataframe["Band"].unique()
    return bands


def update_dataframe_kpoint_coordinates(
    dataframe: pd.DataFrame, kpoint_coordinates: list[list[float, float, float]]
) -> pd.DataFrame:
    """Updates the kpoint coordinates in the dataframe"""
    # add Kx, Ky, Kz columns
    dataframe["Kx"] = np.nan
    dataframe["Ky"] = np.nan
    dataframe["Kz"] = np.nan
    for i, kpoint in enumerate(kpoint_coordinates):
        dataframe.loc[dataframe["Kpoint"] == i, ["Kx", "Ky", "Kz"]] = kpoint
    return dataframe


def get_fermi_surface_kpoint_indices(
    dataframe: pd.DataFrame, bands: list[int]
) -> list[int]:
    """Gets the kpoints that are on the fermi surface"""
    dataframe = dataframe[dataframe["Band"].isin(bands)]
    kpoints = dataframe["Kpoint"].unique()
    return kpoints


efermi = 2.0672
eigs = projected_eigenvalues_from_pickle("/Users/wladerer/Downloads/bi2te3/bi2te3.pkl")
kpoint_coords = kpoints_coordinates_from_vasprun(
    Vasprun(
        "/Users/wladerer/Downloads/bi2te3/vasprun.xml",
        parse_dos=False,
        parse_eigen=False,
        parse_projected_eigen=False,
        parse_potcar_file=False,
    )
)
bands_indices = get_fermi_band_indices(eigs, efermi)
eigs = update_dataframe_kpoint_coordinates(eigs, kpoint_coords)
kpoint_indices = get_fermi_surface_kpoint_indices(eigs, bands_indices)

# Plotting the bands in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(eigs["Kx"], eigs["Ky"], eigs["Kz"], c=eigs["Energy"], cmap="viridis")
ax.set_xlabel("k_x")
ax.set_ylabel("k_y")
ax.set_zlabel("k_z")
plt.show()
