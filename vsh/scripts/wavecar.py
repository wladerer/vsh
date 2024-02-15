from pymatgen.io.vasp import Wavecar
from pymatgen.io.vasp import Poscar
from pymatgen.io.wannier90 import Unk
from itertools import product
import numpy as np


def get_partial_charge_density(wavecar: Wavecar, structure: Poscar, kpoints: list[int], bands: list[int], spins: list[int], spinors: list[int], phases: list[int], scale: float):
    '''Returns the partial charge densities for given kpoints, bands, spins, spinors, phases, and scale.'''
    wave = Wavecar(wavecar)
    poscar = Poscar.from_file(structure)

    combinations = list(product(kpoints, bands, spins, spinors, phases))

    #initialize the first chgcar
    parchg = wave.get_parchg(poscar, *combinations[0], scale=scale)

    #add the rest of the chgcar
    for kpoint, band, spin, spinor, phase in combinations[1:]:
        parchg += wave.get_parchg(poscar, kpoint, band, spin, spinor, phase, scale)

    return parchg

def handle_string_inputs(args, wavecar):
    '''Checks if all is passed as an input and returns a list of all possible values.'''
    args_mapping = {
        'kpoints': (wavecar.nk, list(range(wavecar.nk))),
        'bands': (wavecar.nb, list(range(wavecar.nb))),
        'spins': (wavecar.spin, list(range(wavecar.spin))),
        'spinors': (2, list(range(2))),
        'phases': (2, list(range(2)))
    }

    for arg, (max_value, default_value) in args_mapping.items():
        try:
            if args.__dict__[arg] == 'all':
                args.__dict__[arg] = default_value
            elif ':' in args.__dict__[arg]:
                start, end = map(int, args.__dict__[arg].split(':'))
                args.__dict__[arg] = list(range(start, end+1))
            else:
                args.__dict__[arg] = [int(args.__dict__[arg])]
        except (ValueError, TypeError):
            print(f"Invalid input for {arg}. Please provide a valid input.")

    return args
 

def generate_parchg(args):
    '''Generates a PARCHG file from a WAVECAR file. '''
    wave = Wavecar(args.input)
    poscar = Poscar.from_file(args.structure)
    args = handle_string_inputs(args, wave)
    parchg = get_partial_charge_density(wave, poscar, args.kpoints, args.bands, args.spins, args.spinors, args.phases, args.scale)

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

    functions = {
        'parchg': generate_parchg,
        'mesh': generate_fft_mesh,
        'unk': generate_unk
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)
