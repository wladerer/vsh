import pickle
import uuid
from ase.io import read, write
from PIL import Image
import os

def validate_input(args):
    '''Validates that INCAR, POSCAR, KPOINTS, and POTCAR files are present and formatted correctly'''
    from pymatgen.io.vasp import Incar, Poscar, Kpoints, Potcar
    import os

    # check that each file exists
    directory = args.input
    incar_file = os.path.join(directory, 'INCAR')
    poscar_file = os.path.join(directory, 'POSCAR')
    kpoints_file = os.path.join(directory, 'KPOINTS')
    potcar_file = os.path.join(directory, 'POTCAR')

    for file in [incar_file, poscar_file, kpoints_file, potcar_file]:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"File not found: {file}")
        
    # check that each file is formatted correctly
    incar = Incar.from_file(incar_file)
    poscar = Poscar.from_file(poscar_file)
    kpoints = Kpoints.from_file(kpoints_file)
    potcar = Potcar.from_file(potcar_file)

    #check that incar has valid tags
    incar.check_params() #stdout is empty if no errors


    print("Input files validated successfully")



def snapshot(args):

    if not args.output:
        raise ValueError("No output file specified")
    
    # Create an example atomic structure
    atoms = read(args.snapshot) 
    write('profile_view.png', atoms, rotation='-90x,-90y')
    write('top_view.png', atoms, rotation='0x,0y,-90z')
    write('oblique_view.png', atoms, rotation='10z,-80x,0y')

    # Open the three images
    top_image = Image.open('top_view.png')
    side_image = Image.open('profile_view.png')
    oblique_image = Image.open('oblique_view.png')

    # Get the dimensions of the images
    top_width, top_height = top_image.size
    side_width, side_height = side_image.size
    oblique_width, oblique_height = oblique_image.size

    # Determine the maximum dimensions among the three images
    max_width = max(top_width, side_width, oblique_width)
    max_height = max(top_height, side_height, oblique_height)

    # Create a new blank image with a white background
    combined_image = Image.new('RGB', (max_width * 3, max_height), 'white')

    # Calculate the positions to center each image
    top_position = ((max_width - top_width) // 2, (max_height - top_height) // 2)
    side_position = (max_width, (max_height - side_height) // 2)
    oblique_position = (2 * max_width, (max_height - oblique_height) // 2)

    # Paste the images onto the blank image
    combined_image.paste(top_image, top_position)
    combined_image.paste(side_image, side_position)
    combined_image.paste(oblique_image, oblique_position)

    try:
        combined_image.save(args.output)
        os.remove('profile_view.png')
        os.remove('top_view.png')
        os.remove('oblique_view.png')
        print(f"Saved snapshot to {args.output}")

    except:
        os.remove('profile_view.png')
        os.remove('top_view.png')
        os.remove('oblique_view.png')
        print("Error: Unable to save snapshot")


def parse_general_vasprun(file: str) -> dict:
    '''Parses the general vasprun.xml file for structure, kpoint info, and energy'''
    from pymatgen.io.vasp import Vasprun
    vasprun = Vasprun(file, parse_potcar_file=False, parse_dos=False, parse_eigen=False, parse_projected_eigen=False)

    # Get INCAR parameters
    incar = vasprun.incar
    incar_dict = incar.as_dict()

    # Get KPOINTS parameters
    # kpoints = vasprun.kpoints
    # kpoints_dict = kpoints.as_dict()
    # # if kpoints.labels is None, add a blank label
    # if kpoints_dict['labels'] is None:
    #     kpoints_dict['labels'] = ['']

    # Get initial and final structures
    initial_structure = vasprun.initial_structure
    final_structure = vasprun.final_structure

    # Get energy
    energy = vasprun.final_energy

    # Check if the calculation is converged
    converged = vasprun.converged

    # compile dictionary
    output = {
        "incar": incar_dict,
        # "kpoints": kpoints_dict,
        "initial_structure": initial_structure,
        "final_structure": final_structure,
        "energy": energy,
        "converged": converged
    }

    return output

def note_to_string(file: str) -> str:
    '''Converts a note file to a string'''
    with open(file, 'r') as f:
        note = f.read()
    return note

def unique_serial_number():
    '''Generates a unique serial number for each simulation'''
    return uuid.uuid4()

def write_data_pickle(args):
    '''Stores a snapshot of the simulation in a pickle file. '''
    
    # Get the data dictionary
    data = parse_general_vasprun(args.input)

    if args.note:
        note = note_to_string(args.note)
        data['note'] = note

    if args.electronic_structure:
        from procar import load_dataframe_from_file
        df = load_dataframe_from_file(args.input)
        data['electronic_structure'] = df

    # Generate a unique serial number
    serial_number = unique_serial_number()
    data['serial_number'] = serial_number

    if args.output:
        # Save the data dictionary
        with open(args.output, 'wb') as f:
            pickle.dump(data, f)

    else:
        print(data)


def unpack_pickle(args):
    '''Unpacks POSCAR, INCAR, CONTCAR, and KPOINTS from a pickle file'''
    from pymatgen.io.vasp import Poscar, Incar, Kpoints
    import pandas as pd

    try:
        with open(args.input, 'rb') as f:
            data = pickle.load(f)
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return
    
    # Unpack the data
    incar = Incar.from_dict(data['incar'])
    # kpoints = Kpoints.from_dict(data['kpoints'])
    poscar = Poscar(data['initial_structure'])
    contcar = Poscar(data['final_structure'])
    energy = data['energy']
    converged = data['converged']
    serial_number = data['serial_number']

    # Save the data
    if args.output:
        incar.write_file(args.output + "/INCAR")
        # kpoints.write_file(args.output + "/KPOINTS")
        poscar.write_file(args.output + "/POSCAR")
        contcar.write_file(args.output + "/CONTCAR")

        with open(f"{args.output}/note.vsh", 'w') as f:
            f.write(f"Energy: {energy}\n")
            f.write(f"Converged: {converged}\n")
            f.write(f"Serial Number: {serial_number}\n")
            if 'note' in data.keys():
                f.write(f"Note: {data['note']}\n")


        if 'electronic_structure' in data.keys():
            df = data['electronic_structure']
            pd.to_pickle(df, args.output + "/electronic_structure.pkl")


    else:

        print("INCAR:")
        print(incar)
        # print("KPOINTS:")
        # print(kpoints.kpts)
        print("POSCAR:")
        print(poscar)
        print("CONTCAR:")
        print(contcar)
        print(f"Energy: {energy}")
        print(f"Converged: {converged}")
        print(f"Serial Number: {serial_number}")
        if 'note' in data.keys():
            print(f"Note: {data['note']}")


def run(args):

    functions = { 
        "snapshot": snapshot,
        "archive": write_data_pickle,
        "unarchive": unpack_pickle,
        "validate": validate_input,
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)




