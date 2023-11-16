import pytest
from scripts.analysis import *
from scripts.slab import structure_from_file
from pymatgen.core.structure import Structure

def test_structure_from_file():
    expected_structure = Structure.from_file('test/files/POSCAR')
    actual_structure = structure_from_file('test/files/POSCAR')
    assert expected_structure == actual_structure

if __name__ == '__main__':
    test_structure_from_file()