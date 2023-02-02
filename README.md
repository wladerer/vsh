# vsh
Command line utilities for interacting with VASP

## getNbands
Function to extract the number of bands from an OUTCAR file.

### Input

- The function accepts an optional input, the path to the OUTCAR file.
- If no path is provided, the function assumes that the OUTCAR file is in the current directory (./OUTCAR).

### Output

The function outputs the number of bands present in the OUTCAR file.

## getNatoms
Function to extract the number of atoms from an OUTCAR file.

### Input

- The function accepts an optional input, the path to the OUTCAR file.
- If no path is provided, the function assumes that the OUTCAR file is in the current directory (./OUTCAR).

### Output

The function outputs the number of atoms present in the OUTCAR file.

## getEfermi
Function to extract the Fermi energy from an OUTCAR file.

### Input

- The function accepts an optional input, the path to the OUTCAR file.
- If no path is provided, the function assumes that the OUTCAR file is in the current directory (./OUTCAR).

### Output

The function outputs the Fermi energy from the OUTCAR file.

## getElements
Function to extract the list of elements from a POSCAR file.

### Input

- The function accepts an optional input, the path to the POSCAR file.
- If no path is provided, the function assumes that the POSCAR file is in the current directory (./POSCAR).

### Output

The function outputs the list of elements in the POSCAR file.

## updateTag
Function to update a tag in an INCAR file.

### Input

- The function accepts three inputs:
  1. The tag to be updated.
  2. The new value of the tag.
  3. The path to the INCAR file.

### Output

The function updates the tag in the INCAR file.

## isConverged
Function to check if a VASP job has converged.

### Input

- The function accepts an optional input, the -d flag.
- If the -d flag is provided, the function checks all subdirectories in the current directory for convergence.
- If the -d flag is not provided, the function checks the current directory for convergence.

### Output

The function outputs the directories that have converged, with the message "Directory has converged."

## restartVasp
Function to restart a VASP job.

### Input

- The function accepts an optional input, the -d flag.
- If the -d flag is provided, the function restarts all VASP jobs in the subdirectories of the current directory.
- If the -d flag is not provided, the function restarts the VASP job in the current directory.

### Output

The function updates the INCAR file in each directory to restart the VASP job.




## Configuration

Firstly, update your ~/.bashrc so that the VSHDIR environment variable is set. A configure.sh script has been provided to update your ~/.bashrc so that it knows to source both the v.sh (where all functions are stored) and the vsh/.vshrc file where specific environment variables are set (e.g path to potential files, default incars, and other important defaults).





