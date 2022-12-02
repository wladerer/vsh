#!/bin/bash

# a script used to restart a VASP job

# check if the -d flag is set
if [[ "$1" == "-d" ]]; then
    # save all subdirectories that contain "CONTCAR" files to an array
    subdirs=( $(find . -type f -name "CONTCAR" -exec dirname {} \;) )
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

# update the INCAR file to restart the job, but ignore all dirs in the finished_job_dirs array
for dir in "${subdirs[@]}"; do
    if [[ ! " ${finished_job_dirs[@]} " =~ " ${dir} " ]]; then
        cd "$dir" || exit
        sed -i 's/ISTART = 1/ISTART = 0/g' INCAR
        sed -i 's/ICHARG = 2/ICHARG = 1/g' INCAR
        cd ..
    fi
done

#inform the user that the INCAR has been updated
echo "The INCAR file has been updated to restart the job(s)"


