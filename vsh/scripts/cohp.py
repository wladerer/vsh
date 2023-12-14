import os
from pymatgen.electronic_structure.cohp import CompleteCohp
from pymatgen.electronic_structure.plotter import CohpPlotter
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from mpl_toolkits import axes_grid1


plt.style.use('seaborn-v0_8-colorblind')

def cohp_from_file(args, file):
    '''Returns a CompleteCohp object from a COHP or COBI file. Default format is LOBSTER'''
    cohp = CompleteCohp.from_file(fmt=args.format, filename=file, structure_file=args.structure, are_cobis=args.cobi) 
    
    return cohp


def cohp_from_dir(directory: str):
    '''Returns a CompleteCohp object from a directory containing a COHP or COBI file. Default format is LOBSTER'''
    
    cohp = CompleteCohp.from_file(fmt='LOBSTER', filename=directory+'/COHPCAR.lobster', structure_file=directory+'/POSCAR') 
    
    return cohp

def ichop_list_to_dataframe(file_path):
    '''Returns a pandas dataframe of the species in the ICOHPLIST.lobster file'''
    
    df = pd.read_csv(file_path, sep='\s+', skiprows=1, names=['COHP', 'atom_Mu', 'atom_Nu', 'distance', 'translation_x', 'translation_y', 'translation_z', 'ICOHP'])
    
    return df

def check_cohp_path(input_path):
    '''Checks if the input path is a file or directory and returns the path to the ICOHPLIST.lobster file'''
    if os.path.isfile(input_path):
        file_path = input_path
    elif os.path.isdir(input_path):
        file_path = os.path.join(input_path, 'ICOHPLIST.lobster')
    else:
        raise ValueError("Invalid input. Please provide a valid file path or directory.")
    
    return file_path


def show_cohp_species(input_path):
    '''Prints a list of the species in the ICOHPLIST.lobster file'''
    
    input_path = os.path.abspath(input_path)
    file_path = check_cohp_path(input_path)
    df = ichop_list_to_dataframe(file_path)

    return None


def icohp_to_pickle(args):
    '''Saves ICOHP data to a pickle file'''

    #check if len(args.input) == len(args.output)
    if len(args.input) != len(args.output):
        raise ValueError("Number of input files and output files do not match.")

    for input_path, output in zip(args.input, args.output):
        input_path = os.path.abspath(input_path)
        file_path = check_cohp_path(input_path)
        df = ichop_list_to_dataframe(file_path)
        
        #save to pickle file
        df.to_pickle(output)

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

def get_icohp_graph(args) -> list[nx.Graph]:
    '''Plots a graph of the COHP or COBI files'''
    graphs = []

    for input_path in args.input:
        input_path = os.path.abspath(input_path)
        file_path = check_cohp_path(input_path)
        df = ichop_list_to_dataframe(file_path)

        G = nx.from_pandas_edgelist(df, 'atom_Mu', 'atom_Nu', 'ICOHP')
        graphs.append(G)

    return graphs

def plot_icohp_graph(args):
    '''Plots a graph of the COHP or COBI file'''

    graphs = get_icohp_graph(args)

    for G in graphs:
        #color edges by weight using a colormap
        pos = nx.spring_layout(G)
        edges = G.edges()
        weights = [G[u][v]['ICOHP'] for u,v in edges]
        nx.draw(G, pos, edge_color=weights, width=2, edge_cmap=plt.cm.plasma)
        pathcollection = nx.draw_networkx_nodes(G, pos, node_size=600, node_color='black')
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', font_color='white')
        plt.axis('off')
        
        plt.show()

def run(args):
    functions = {
        "plot": plot_cohps,
        "list": show_cohp_species,
        "pickle": icohp_to_pickle,
        "graph": plot_icohp_graph
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)

    return None
    



