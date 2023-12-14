import os
from pymatgen.electronic_structure.cohp import CompleteCohp
from pymatgen.electronic_structure.plotter import CohpPlotter
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-colorblind')

def cohp_from_file(args, file):
    '''Returns a CompleteCohp object from a COHP or COBI file. Default format is LOBSTER'''
    cohp = CompleteCohp.from_file(fmt=args.format, filename=file, structure_file=args.structure, are_cobis=args.cobi) 
    
    return cohp


def cohp_from_dir(directory: str):
    '''Returns a CompleteCohp object from a directory containing a COHP or COBI file. Default format is LOBSTER'''
    
    cohp = CompleteCohp.from_file(fmt='LOBSTER', filename=directory+'/COHPCAR.lobster', structure_file=directory+'/POSCAR') 
    
    return cohp

def show_cohp_species(input: str):
    '''Prints a list of the species in the ICOHPLIST.lobster file'''
    input = os.path.abspath(input)

    if os.path.isfile(input):
        file_path = input
    elif os.path.isdir(input):
        file_path = os.path.join(input, 'ICOHPLIST.lobster')
    else:
        raise ValueError("Invalid input. Please provide a valid file path or directory.")

    os.system('cat ' + file_path)

    return None

def list_species(args):
    '''Prints a list of the species in the ICOHPCAR.lobster file'''
    
    for input in args.input:
        show_cohp_species(input)

    return None

def collate_cohps(args):
    '''Collates a list of COHP or COBI files. Default format is LOBSTER'''
    plotter = CohpPlotter(are_cobis=args.cobi)
    
    cohp_list = [cohp_from_dir(directory) for directory in args.input ] 
    
    for cohp_object in cohp_list:
        plotter.add_cohp(label=args.label, cohp=cohp_object.get_cohp_by_label(str(args.label)))
        
    return plotter

def plot_cohps(args):
    '''Plots a list of COHP or COBI files. Default format is LOBSTER'''

    cohp_plt = collate_cohps(args)
    
    if args.output:
        #convert cohp_plot to an ax object
        plot = cohp_plt.get_plot(args.integrated)
        plot.figure.savefig(args.output, dpi=args.dpi)
        
    else:
        cohp_plt.show()
    
    return None

def run(args):
    functions = {
        "plot": plot_cohps,
        "list": list_species
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)

    return None
    



