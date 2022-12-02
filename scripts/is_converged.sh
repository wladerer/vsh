#!/bin/bash

# a script to check uf a job has converged
# has an optional flag to check all subdirectories in the current directory ( -d )

# check if the -d flag is set
if [[ "$1" == "-d" ]]; then
    # save all subdirectories that contain "CONTCAR" files to an array
    subdirs=( $(find . -type f -name "OUTCAR" -exec dirname {} \;) )
else
    # save the current directory to an array
    subdirs=( $(pwd) )
fi

# for each subrirectory in the array , check if the OUTCAR file contains "reached required accuracy", if so , add it to an array calldd finished_job_dirs
finished_job_dirs=()

for subdir in "${subdirs[@]}"; do
    if grep -q "reached required accuracy" "$subdir/OUTCAR"; then
        finished_job_dirs+=("$subdir")
    fi
done

# print the directories that have converged
for dir in "${finished_job_dirs[@]}"; do
    echo "$dir" has converged
done