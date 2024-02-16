from itertools import product

import numpy as np
from pymatgen.io.vasp import Poscar, Wavecar
from pymatgen.io.wannier90 import Unk


def parse_spins(spin_channel_str: str):
    if spin_channel_str in ["0", "1"]:
        return int(spin_channel_str)
    elif spin_channel_str in ["up", "down"]:
        # Handle 'up' or 'down' accordingly (this may also be a spinor)
        return 0 if spin_channel_str == "up" else 1
    elif spin_channel_str is None:
        return None
    else:
        raise ValueError("Invalid spin channel value")


def get_partial_charge_density(
    wavecar: Wavecar,
    poscar: Poscar,
    kpoints: list[int],
    bands: list[int],
    spins: list[int],
    spinors: list[int],
    phases: list[int],
    scale: float,
):
    """Returns the partial charge densities for given kpoints, bands, spins, spinors, phases, and scale."""

    specifications = [kpoints, bands, spins, spinors, phases]
    # check if any of the specications are None or list[None], if so, remove them
    for i, spec in enumerate(specifications):
        if spec is None:
            specifications[i] = [None]
        elif isinstance(spec, int):
            specifications[i] = [spec]

    combinations = list(product(*specifications))

    # initialize the first chgcar
    parchg = wavecar.get_parchg(poscar, *combinations[0], scale=scale)

    # add the rest of the chgcar
    for kpoint, band, spin, spinor, phase in combinations[1:]:
        parchg += wavecar.get_parchg(poscar, kpoint, band, spin, spinor, phase, scale)

    return parchg


def generate_parchg(args):
    """Generates a PARCHG file from a WAVECAR file."""
    wave = Wavecar(args.input)
    poscar = Poscar.from_file(args.structure)

    # sanitize the input

    spins = parse_spins(args.spin)
    spinor = parse_spins(args.spinor)

    # check if the range of bands and kpoints exceeds the number of bands and kpoints
    if args.bands and max(args.bands) > wave.nb:
        raise ValueError(
            f"Maximum band index {max(args.bands)} exceeds the number of bands {wave.nb}"
        )
    if args.kpoints and max(args.kpoints) > wave.nk:
        raise ValueError(
            f"Maximum kpoint index {max(args.kpoints)} exceeds the number of kpoints {wave.nk}"
        )

    parchg = get_partial_charge_density(
        wave, poscar, args.kpoints, args.bands, spins, spinor, args.phase, args.scale
    )

    if args.output:
        if args.cube:
            parchg.to_cube(args.output)
        else:
            parchg.write_file(args.output)
    else:
        print(parchg.__str__())


# def generate_fft_mesh(args):
#     '''Generates a COEFFS file from a WAVECAR file. '''
#     mesh = Wavecar(args.input).fft_mesh(args.kpoints, args.bands, args.spins, args.spinors)
#     evals = np.fft.ifftn(mesh)
#     if args.output:
#         np.save(args.output, evals)
#     else:
#         print(evals)


def generate_unk(args):
    """
    This is a modified version of the generate_unk method from the pymatgen

    Write the UNK files to the given directory.

    Writes the cell-periodic part of the bloch wavefunctions from the
    WAVECAR file to each of the UNK files. There will be one UNK file for
    each of the kpoints in the WAVECAR file.

    Note:
        wannier90 expects the full kpoint grid instead of the symmetry-
        reduced one that VASP stores the wavefunctions on. You should run
        a nscf calculation with ISYM=0 to obtain the correct grid.

    Args:
        directory (str): directory where the UNK files are written
    """
    if not args.output:
        raise ValueError("Output filename must be specified.")

    wavecar = Wavecar(args.input)

    N = np.prod(wavecar.ng)
    for ik in range(wavecar.nk):
        fname = f"UNK{ik+1:05d}."
        if wavecar.vasp_type.lower()[0] == "n":
            data = np.empty((wavecar.nb, 2, *wavecar.ng), dtype=np.complex128)
            for ib in range(wavecar.nb):
                data[ib, 0, :, :, :] = (
                    np.fft.ifftn(wavecar.fft_mesh(ik, ib, spinor=0)) * N
                )
                data[ib, 1, :, :, :] = (
                    np.fft.ifftn(wavecar.fft_mesh(ik, ib, spinor=1)) * N
                )
            Unk(ik + 1, data).write_file(f"{args.output}_{fname}")
        else:
            data = np.empty((wavecar.nb, *wavecar.ng), dtype=np.complex128)
            for ispin in range(wavecar.spin):
                for ib in range(wavecar.nb):
                    data[ib, :, :, :] = (
                        np.fft.ifftn(wavecar.fft_mesh(ik, ib, spin=ispin)) * N
                    )
                Unk(ik + 1, data).write_file(f"{args.output}_{fname}{ispin+1}")


def print_number_of_kpoints(args):
    wave = Wavecar(args.input)
    print(f"{wave.nk}")


def print_number_of_bands(args):
    wave = Wavecar(args.input)
    print(f"{wave.nb}")


def print_fermi_energy(args):
    wave = Wavecar(args.input)
    print(f"{wave.efermi}")


def get_band_occupancy_info(wavecar: Wavecar):
    """Gets the band occupancy information from a WAVECAR file."""
    import pandas as pd

    band_energy = wavecar.band_energy
    dfs = []
    for kpoint, bands in enumerate(band_energy):
        df = pd.DataFrame(bands, columns=["energy", "idk", "occupancy"])
        df["kpoint"] = kpoint

        # Update each row of bands to include band index (starting at 0)
        for i, row in df.iterrows():
            df.at[i, "band"] = i

        dfs.append(df)

    df = pd.concat(dfs)

    # Sum the occupation of each band and divide by the number of kpoints to get a relative occupancy
    df["relative_occupancy"] = (
        df.groupby("band")["occupancy"].transform("sum") / wavecar.nk
    )

    # Drop the kpoint and idk columns
    df = df.drop(columns=["kpoint", "idk", "occupancy"])
    # Remove duplicate bands
    df = df.drop_duplicates()

    return df[df["relative_occupancy"] > 0].tail(19)


def print_band_occupancy_info(args):
    wave = Wavecar(args.input)
    df = get_band_occupancy_info(wave)
    # print dataframe without index

    print(df.to_string(index=False))


def run(args):
    functions = {
        "parchg": generate_parchg,
        "unk": generate_unk,
        "nk": print_number_of_kpoints,
        "nb": print_number_of_bands,
        "efermi": print_fermi_energy,
        "occ": print_band_occupancy_info,
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)
