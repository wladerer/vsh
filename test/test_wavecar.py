import unittest
from unittest.mock import patch
from vsh.scripts.wavecar import handle_string_inputs
from pymatgen.io.vasp.outputs import Wavecar
import argparse

test_wavecar1_file = '/Users/wladerer/research/pt3sn/bulk/WAVECAR'
test_poscar1_file = '/Users/wladerer/research/pt3sn/bulk/POSCAR'

# nk = 180, nb =112, spin =1
test_wavecar2_file = '/Users/wladerer/research/tetrads/bi2te3/band/WAVECAR'
test_poscar2_file = '/Users/wladerer/research/tetrads/bi2te3/band/POSCAR'

#lets get some info from the wavecar file
wave = Wavecar(test_wavecar1_file)
print(wave.nk, wave.nb, wave.spin)