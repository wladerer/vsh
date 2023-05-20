import pytest
from analysis import *

def test_get_adjacency_matrix():
    atoms = Atoms('H2', positions=[[0, 0, 0], [0, 0, 1]])
    adjacency_matrix = get_adjacency_matrix(atoms)
    assert adjacency_matrix[0][1] == 1

    atoms = Atoms()
    with pytest.raises(ValueError):
        adjacency_matrix = get_adjacency_matrix(atoms)


if __name__ == '__main__':
    test_get_adjacency_matrix()
