import pytest
from vsh.scripts.analysis import *

def test_check_convergence():
    assert check_convergence(file='files/vasprun.xml') == [True, True]



if __name__ == '__main__':
    test_check_convergence()
