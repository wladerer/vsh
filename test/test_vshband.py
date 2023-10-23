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

test_handle_atoms()