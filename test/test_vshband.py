from ase.io import read
from os.path import abspath, dirname, join
from vsh.scripts.band import *


def test_handle_atoms():
    # read the test file
    atom_indices = handle_atoms('test/files/wp2CO.vasp')

    # check if the atom types and counts match the expected values
    assert len(atom_indices) == 4
    assert atom_indices['P'] == [i for i in range(48)]
    assert atom_indices['W'] == [i for i in range(48, 72)]
    assert atom_indices['C'] == [72]
    assert atom_indices['O'] == [73]

    # test with a different file
    atom_indices = handle_atoms('test/files/Cu2O.vasp')

    # check if the atom types and counts match the expected values
    assert len(atom_indices) == 2
    assert atom_indices['Cu'] == [i for i in range(4)]
    assert atom_indices['O'] == [i for i in range(4, 6)]


def test_handle_orbitals():
    # test with 's'
    orbitals = 's'
    expected_output = [0]
    assert handle_orbitals(orbitals) == expected_output

    # test with 'p'
    orbitals = 'p'
    expected_output = [1, 2, 3]
    assert handle_orbitals(orbitals) == expected_output

    # test with 'd'
    orbitals = 'd'
    expected_output = [4, 5, 6, 7, 8]
    assert handle_orbitals(orbitals) == expected_output

    # test with 'f'
    orbitals = 'f'
    expected_output = [9, 10, 11, 12, 13, 14, 15]
    assert handle_orbitals(orbitals) == expected_output

    # test with 'all'
    orbitals = 'all'
    expected_output = list(range(16))
    assert handle_orbitals(orbitals) == expected_output


if __name__ == '__main__':
    test_handle_atoms()
    test_handle_orbitals()
