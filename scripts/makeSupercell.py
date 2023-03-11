from ase.io import read, write
from ase.build.supercells import make_supercell
import sys


def makeSupercell(M, POSCAR: str = './POSCAR') -> None:
    '''
    Creates a supercell from a POSCAR file
    '''
    cell = read(POSCAR)
    supercell = make_supercell(cell, M)
    write('supercell.poscar', supercell, vasp5=True, sort=True)


if __name__ == "__main__":

    poscar = sys.argv[1]
    
    x_rep = int(sys.argv[2])
    y_rep = int(sys.argv[3])
    z_rep = int(sys.argv[4])

    if x_rep < 1 or y_rep < 1 or z_rep < 1:
        raise ValueError('Replication factors must be positive integers')
    
    M = [[x_rep, 0, 0], [0, y_rep, 0], [0, 0, z_rep]]
    
    makeSupercell(M, poscar)
