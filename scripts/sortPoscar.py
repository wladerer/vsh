from pymatgen.io.vasp import Poscar
import sys 

def sort(poscar_file: str) -> Poscar:
    structure = Poscar.from_file(poscar_file).structure
    poscar = Poscar(structure, sort_structure=True)
    poscar.write_file(poscar_file)

if __name__ == "__main__":
    poscar = sys.argv[1]
    sort(poscar)