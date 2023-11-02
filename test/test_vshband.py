from ase.io import read
from os.path import abspath, dirname, join
from vshband import handle_atoms


def test_handle_atoms():
    # read the test file
    test_file = abspath(join(dirname(__file__), 'files', 'wp2CO.vasp'))
    atom_indices = handle_atoms(test_file)

    # check if the atom types and counts match the expected values
    assert len(atom_indices) == 4
    assert atom_indices['P'] == [i for i in range(48)]
    assert atom_indices['W'] == [i for i in range(48, 72)]
    assert atom_indices['C'] == [72]
    assert atom_indices['O'] == [73]

    # test with a different file
    test_file = abspath(join(dirname(__file__), 'files', 'Cu2O.vasp'))
    atom_indices = handle_atoms(test_file)

    # check if the atom types and counts match the expected values
    assert len(atom_indices) == 2
    assert atom_indices['Cu'] == [i for i in range(8)]
    assert atom_indices['O'] == [i for i in range(8, 16)]


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