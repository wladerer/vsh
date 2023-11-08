import subprocess


def archive_output(files: list, archive_name: str):
    """Archives a list of files into a tarball"""
    try:
        # Create a tarball of the output files
        result = subprocess.run(
            ["tar", "-czvf", archive_name + ".tgz"] + files,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Print the output of the tar command
        print(result.stdout)

    except subprocess.CalledProcessError:
        print("Error: Unable to archive output files.")


def copy_output(file: str, destination: str):
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


 