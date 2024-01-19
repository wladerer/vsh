from pymatgen.io.vasp import Wavecar
from pymatgen.io.vasp import Poscar
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

def run(args):
    if args.parchg:
        generate_parchg(args)
    
    if args.mesh:
        generate_fft_mesh(args)

        



