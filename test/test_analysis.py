import pytest
from ..analysis import *

def test_get_adjacency_matrix():
    atoms = Atoms('H2', positions=[[0, 0, 0], [0, 0, 1]])
    adjacency_matrix = get_adjacency_matrix(atoms)
    assert adjacency_matrix[0][1] == 1

    atoms = Atoms()
    with pytest.raises(ValueError):
        adjacency_matrix = get_adjacency_matrix(atoms)

def test_get_conflicting_atoms():
    atoms = Atoms('H2', positions=[[0, 0, 0], [0, 0, 1]])
    conflicts = conflicting_atoms(atoms, 1.1)
    assert conflicts == {'H0-H1': 1.0}

    atoms = Atoms('H2', positions=[[0, 0, 0], [0, 0, 1]])
    conflicts = conflicting_atoms(atoms, 0.9)
    assert conflicts == None

    #load atoms from a test file
    atoms = read('/home/wladerer/github/vsh/tests/files/wp2CO.vasp')
    conflicts = conflicting_atoms(atoms,  1.5)
    assert conflicts == {'C72-O73': 1.123000000000001, 'O73-C72': 1.123000000000001}
    
    conflicts = conflicting_atoms(atoms, 3)


if __name__ == '__main__':
    test_get_adjacency_matrix()
    test_get_conflicting_atoms()
