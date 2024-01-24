#!/bin/bash

# Exit if any command fails
set -e

# Check that poscar argument is provided
if [ -z "$1" ]; then
    echo "Error: No poscar argument provided."
    exit 1
fi

poscar=POSCAR
potcar=POTCAR
kpoints=KPOINTS
geom_incar=geom.incar
sod_incar=sod.incar
soc_incar=soc.incar

mkdir -p geom sod soc

# Function to check if a file exists and is not empty
check_file() {
    local file=$1
    if [[ ! -e "$file" ]]; then
        echo "Error: File $file does not exist."
        exit 1
    elif [[ ! -s "$file" ]]; then
        echo "Error: File $file is empty."
        exit 1
    fi
}

# Function to copy a file to multiple directories
copy_to_dirs() {
    local file=$1
    check_file "$file"
    shift
    for dir in "$@"; do
        cp "$file" "$dir"
    done
}

# Copy potcar and kpoints to each directory
copy_to_dirs $potcar geom/POTCAR sod/POTCAR soc/POTCAR 
copy_to_dirs $kpoints geom/KPOINTS sod/KPOINTS soc/KPOINTS

# Copy incar to each directory
copy_to_dirs $geom_incar geom/INCAR
copy_to_dirs $sod_incar sod/INCAR
copy_to_dirs $soc_incar soc/INCAR

# Copy poscar to geom
cp "$poscar" geom/POSCAR