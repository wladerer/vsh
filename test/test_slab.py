import pytest
from vsh.scripts.analysis import *
from vsh.scripts.slab import structure_from_file
from pymatgen.core.structure import Structure

def test_structure_from_file():
    expected_structure = Structure.from_file('files/POSCAR')
    actual_structure = structure_from_file('files/POSCAR')
    assert expected_structure == actual_structure

if __name__ == '__main__':
    test_structure_from_file()