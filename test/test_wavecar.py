import unittest
from unittest.mock import patch
from pymatgen.io.vasp.outputs import Wavecar
import argparse

"""
    Attributes:
        filename (str): String of the input file (usually WAVECAR).
        vasp_type (str): String that determines VASP type the WAVECAR was generated with.
            One of 'std', 'gam', 'ncl'.
        nk (int): Number of k-points from the WAVECAR.
        nb (int): Number of bands per k-point.
        encut (float): Energy cutoff (used to define G_{cut}).
        efermi (float): Fermi energy.
        a (numpy.ndarray): Primitive lattice vectors of the cell (e.g. a_1 = self.a[0, :]).
        b (numpy.ndarray): Reciprocal lattice vectors of the cell (e.g. b_1 = self.b[0, :]).
        vol (float): The volume of the unit cell in real space.
        kpoints (numpy.ndarray): The list of k-points read from the WAVECAR file.
        band_energy (list): The list of band eigenenergies (and corresponding occupancies) for each kpoint,
            where the first index corresponds to the index of the k-point (e.g. self.band_energy[kp]).
        Gpoints (list): The list of generated G-points for each k-point (a double list), which
            are used with the coefficients for each k-point and band to recreate
            the wavefunction (e.g. self.Gpoints[kp] is the list of G-points for
            k-point kp). The G-points depend on the k-point and reciprocal lattice
            and therefore are identical for each band at the same k-point. Each
            G-point is represented by integer multipliers (e.g. assuming
            Gpoints[kp][n] == [n_1, n_2, n_3], then
            G_n = n_1*b_1 + n_2*b_2 + n_3*b_3)
        coeffs (list): The list of coefficients for each k-point and band for reconstructing the wavefunction.
            For non-spin-polarized, the first index corresponds to the kpoint and the second corresponds to the band
            (e.g. self.coeffs[kp][b] corresponds to k-point kp and band b). For spin-polarized calculations,
            the first index is for the spin. If the calculation was non-collinear, then self.coeffs[kp][b] will have
            two columns (one for each component of the spinor).
"""


bi2se3_wavecar = "/home/wladerer/github/vsh/test/files/Bi2Se3/WAVECAR"
bi2se3_poscar = "/home/wladerer/github/vsh/test/files/Bi2Se3/POSCAR"
# nk = 6, nb = 64, spin = 1, efermi = 4.0126579574404495, encut = 600.0
# lets get some info from the wavecar file
import pandas as pd
from pymatgen.io.vasp.outputs import Wavecar


def get_band_occupancy_info(wavecar: Wavecar):
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


wavecar = Wavecar(bi2se3_wavecar)
df = get_band_occupancy_info(wavecar)
print(df)
