from pymatgen.io.vasp import Wavecar
from pymatgen.io.vasp import Poscar
from pymatgen.io.wannier90 import Unk
import numpy as np


def generate_parchg(args):
    '''Generates a PARCHG file from a WAVECAR file. '''
    wave = Wavecar(args.input)
    poscar = Poscar.from_file(args.structure)

    chgcar = wave.get_parchg(poscar, args.kpoint, args.band, args.spin, args.spinor, args.phase, args.scale)

    if args.output:
        if args.cube:
            chgcar.to_cube(args.output)
        else: 
            chgcar.write_file(args.output)
    else:
        print(chgcar.__str__())

def generate_fft_mesh(args):
    '''Generates a COEFFS file from a WAVECAR file. '''
    mesh = Wavecar(args.input).fft_mesh(args.kpoint, args.band, args.spin, args.spinor, args.shift)
    evals = np.fft.ifftn(mesh)
    if args.output:
        np.save(args.output, evals)
    else:
        print(evals)

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
                data[ib, 0, :, :, :] = np.fft.ifftn(wavecar.fft_mesh(ik, ib, spinor=0)) * N
                data[ib, 1, :, :, :] = np.fft.ifftn(wavecar.fft_mesh(ik, ib, spinor=1)) * N
            Unk(ik + 1, data).write_file(f"{args.output}_{fname}")
        else:
            data = np.empty((wavecar.nb, *wavecar.ng), dtype=np.complex128)
            for ispin in range(wavecar.spin):
                for ib in range(wavecar.nb):
                    data[ib, :, :, :] = np.fft.ifftn(wavecar.fft_mesh(ik, ib, spin=ispin)) * N
                Unk(ik + 1, data).write_file(f"{args.output}_{fname}{ispin+1}")

def run(args):
    if args.parchg:
        generate_parchg(args)
    
    if args.mesh:
        generate_fft_mesh(args)

    if args.unk:
        generate_unk(args)


        



