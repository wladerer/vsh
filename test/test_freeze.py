import pytest
import numpy as np
from ase import Atoms
from scripts.freeze import calculate_vacuum
from ase.build import fcc111

slab_10a = fcc111('Al', size=(2,2,3), vacuum=10.0)
slab_no_vacuum = fcc111('Al', size=(2,2,3), vacuum=0.0)

def test_calculate_vacuum():
    # Test case 1: 10 Angstrom vacuum
    vacuum = calculate_vacuum(slab_10a)
    assert vacuum == 10.0

    # Test case 2: 0 Angstrom vacuum
    vacuum = calculate_vacuum(slab_no_vacuum)
    assert vacuum == 0.0