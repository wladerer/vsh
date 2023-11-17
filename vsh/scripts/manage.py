import subprocess
from ase.io import read, write
from PIL import Image
import os

def archive(files: list, archive_name: str):
    """Archives a list of files into a tarball"""
    try:
        # Create a tarball of the output files
        
        result = subprocess.run(
            ["tar", "-czvf", archive_name] + files,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Print the output of the tar command
        print(result.stdout)
        print(f"Created archive: {archive_name}")

    except subprocess.CalledProcessError:
        print("Error: Unable to archive output files.")


def copy(file: str, destination: str):
    """Copies a file to a destination"""
    try:
        # Copy the file to the destination
        result = subprocess.run(
            ["cp", file, destination],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Print the output of the cp command
        print(result.stdout)

    except subprocess.CalledProcessError:
        print("Error: Unable to copy output file.")

    except FileNotFoundError:
        print("Error: Unable to find output file.")

    except IsADirectoryError:
        print("Error: Destination is a directory.")


def copy_job(args):
    """Copies all relevant job files to a destination"""
    try:
        files = ["POSCAR", "INCAR", "POTCAR", "KPOINTS", "CONTCAR"]
        # Get only the output files that exist
        files = [file for file in files if os.path.exists(file)]

        # Remove any excluded files
        files = [file for file in files if file not in args.exclude]

        # Copy the output files, renaming CONTCAR to POSCAR if requested
        for file in files:
            if file == "CONTCAR" and args.rename_contcar:
                copy(file, os.path.join(args.destination, "POSCAR"))
                print(f"Renamed CONTCAR to POSCAR and copied to {args.destination}")
            else:
                copy(file, args.destination)

        print(f"Copied files: {files} to {args.destination}")

    except subprocess.CalledProcessError:
        print("Error: Unable to copy output files.")

def archive_job(args):
    """Archives all relevant job files into a tarball"""
    try:
        files = ["OUTCAR", "POSCAR", "INCAR", "vasprun.xml", "KPOINTS", "CONTCAR", "vaspout.h5", "PROCAR"]
        # Get only the output files that exist
        files = [file for file in files if os.path.exists(file)]

        # Remove any excluded files
        files = [file for file in files if file not in args.exclude]

        # Archive the output files
        archive(files, args.output)

    except subprocess.CalledProcessError:
        print(f"Error: Unable to archive output files: {files}")

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

def run(args):

    functions = { 
        "archive": archive_job,
        "copy": copy_job,
        "snapshot": snapshot
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)




