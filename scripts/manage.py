import subprocess
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


def run(args):

    functions = { 
        "archive": archive_job,
        "copy": copy_job
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)




