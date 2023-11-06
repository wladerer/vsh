import pytest
from scripts.analysis import *

def test_check_convergence():
    assert check_convergence(file=) == [True, True]


if __name__ == '__main__':
    test_get_adjacency_matrix()
    test_get_conflicting_atoms()
