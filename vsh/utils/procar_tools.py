from vsh.scripts.procar import load_dataframe_from_file, add_kpoint_labels
from pymatgen.io.vasp import Vasprun
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.core.structure import Structure


# get ions from vasprun
def get_ions(vasprun: Vasprun):
    """Get the ions from a vasprun file"""
    return vasprun.atomic_symbols


def get_compositional_variation(file: str, band: int):
    """Get compositional variation of a band"""
    dataframe = load_dataframe_from_file(file)
    dataframe = dataframe[dataframe["Band"] == int(band)]
    dataframe = dataframe.groupby(["Spin", "Kpoint", "Band", "Ion"]).sum().reset_index()

    for kpoint in dataframe["Kpoint"].unique():
        kpoint_data = dataframe[dataframe["Kpoint"] == int(kpoint)]
        kpoint_data["Percent"] = kpoint_data["Value"] / kpoint_data["Value"].sum() * 100
        dataframe.loc[dataframe["Kpoint"] == int(kpoint), "Percent"] = kpoint_data[
            "Percent"
        ]

    return dataframe


def plot_compositional_variation(file: str, band: int, labels: list[str] = None):
    """Plots the compositional variation of a band"""
    dataframe = get_compositional_variation(file, band)
    # plot each ion percentage against kpoints
    import plotly.graph_objects as go

    fig = go.Figure()
    for ion in dataframe["Ion"].unique():
        ion_data = dataframe[dataframe["Ion"] == ion]
        fig.add_trace(
            go.Scatter(
                x=ion_data["Kpoint"],
                y=ion_data["Percent"],
                mode="lines",
                name=f"Ion {ion}",
            )
        )

    fig.update_layout(
        title=f"Band {band} Ion Variation",
        xaxis_title="Kpoint",
        yaxis_title="Ion Contribution (%)",
    )

    if labels:
        add_kpoint_labels(fig, dataframe, labels)

    fig.show()


def get_equivalent_positions(pmg_structure):
    """Get the equivalent positions of a structure"""
    from pymatgen.core.structure import Structure
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

    spacegroup = SpacegroupAnalyzer(pmg_structure)
    sym_structure = spacegroup.get_symmetrized_structure()
    sites = sym_structure.equivalent_sites

    for site in sites:
        print(f"Type: {site[0].species_string} \t Count: {len(site)}")

    return None
