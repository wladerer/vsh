from py4vasp.data import Band, Structure, Topology
import pandas as pd
import plotly.graph_objs as go

# this module is meant to be used as an api for the py4vasp package - it is not meant to be run as a script
# most of these functions require the user to tinker with their data and inspect the output


def atoms_by_height(file: str):
    """Prints the atoms in the order of their height."""
    coords = Structure.from_file(file).cartesian_positions()
    atoms = Topology.from_file(file).elements()

    return pd.DataFrame({"atoms": atoms, "height": coords[:, 2]}).sort_values("height")


def band_to_df(file: str, selection: str | None = None):
    """Returns a pandas dataframe of the band structure data."""
    band_data = Band.from_file(file)
    band_info = band_data.to_frame(selection=selection)

    return band_info


def get_band_plot(file: str, selection: str | None = None):
    """Plots the band structure data."""
    band_data = Band.from_file(file)
    plot = band_data.to_plotly(selection=selection)
    fig = go.Figure(data=plot)

    return fig


def plot_band(file: str, selection: str | None = None):
    """Plots the band structure data."""
    fig = get_band_plot(file, selection=selection)
    fig.show()
