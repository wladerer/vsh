import numpy as np

def get_vasp_data(file: str, reference_correction: int = 1) -> dict:
    """Pulls data from a vasprun.xml file and returns it as a dictionary."""
    from pymatgen.io.vasp import Vasprun
    from pymatgen.core.structure import Structure

    vasprun = Vasprun(file)
    structure = vasprun.final_structure
    energy = vasprun.final_energy / reference_correction
    electronic = vasprun.converged_electronic
    ionic = vasprun.converged_ionic

    data = { "structure": structure, "energy": energy, "electronic": electronic, "ionic": ionic }

    return data

class Reaction:

    def __init__(self, reactants: list[dict], products: list[dict]) -> None:
        self.reactants: list[dict] = reactants
        self.products: list[dict] = products

    @property
    def binding_energy(self) -> float:
        total_reactant_energy = np.sum([ reactant["energy"] for reactant in self.reactants ])
        total_product_energy = np.sum([ product["energy"] for product in self.products ])
        binding_energy = total_product_energy - total_reactant_energy

        return binding_energy
    
    def reactant_from_file(self, file: str, reference_correction: int = 1) -> None:
        reactant = get_vasp_data(file, reference_correction)
        self.reactants.append(reactant)

    def product_from_file(self, file: str, reference_correction: int = 1) -> None:
        product = get_vasp_data(file, reference_correction)
        self.products.append(product)

    def reactant_from_dict(self, data: dict) -> None:
        self.reactants.append(data)

    def product_from_dict(self, data: dict) -> None:
        self.products.append(data)

    @classmethod
    def reaction_from_csv(cls, file: str):
        import pandas as pd

        df = pd.read_csv(file)

        for index, row in df.iterrows():

            #format is type, filepath, reference_correction
            if row["type"] == "reactant" or "r":
                cls.reactant_from_file(row["filepath"], row["reference_correction"])
            elif row["type"] == "product" or "p":
                cls.product_from_file(row["filepath"], row["reference_correction"])
            else:
                raise ValueError("Invalid type in CSV file.")
            
    

            

            
        
            


    
    
    

