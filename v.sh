#!/bin/bash

function getNbands {

    #if $1 is empty, then assume $1=./

    if [ -z "$1" ]; then
        outcar=./OUTCAR
    else
        outcar=$1
    fi
    grep NBANDS $outcar | awk -F " " '{print $NF}'
}

function updateTag {

    # check if the $1 or $2 variables are the incar file
    # if so, then inform the user that the order of arguments is $1 = tag, $2 = value, $3 = incar file
    #check for the substring INCAR in the whole string

    if [[ "$1" == *"INCAR"* ]]; then
        echo "The order of arguments is \n updateTag tag value INCAR_file"
        exit
    fi

    tag=$1
    value=$2
    sed "s/${tag}.*/${tag} = ${value}/g" $incar
    sed -i "s/${tag}.*/${tag} = ${value}/g" $incar
}

function isConverged {

    # a script to check uf a job has converged
    # has an optional flag to check all subdirectories in the current directory ( -d )

    # check if the -d flag is set
    if [[ "$1" == "-d" ]]; then
        # save all subdirectories that contain "CONTCAR" files to an array
        subdirs=($(find . -type f -name "OUTCAR" -exec dirname {} \;))
    else
        # save the current directory to an array
        subdirs=($(pwd))
    fi

    # for each subrirectory in the array , check if the OUTCAR file contains "reached required accuracy",     if so , add it to an array calldd finished_job_dirs
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
}

function restartVasp {

    # check if the -d flag is set
    if [[ "$1" == "-d" ]]; then
        # save all subdirectories that contain "CONTCAR" files to an array
        subdirs=($(find . -type f -name "CONTCAR" -exec dirname {} \;))
    else
        # save the current directory to an array
        subdirs=($(pwd))
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
            sed 's/ISTART = 1/ISTART = 0/g' INCAR
            sed 's/ICHARG = 2/ICHARG = 1/g' INCAR
            sed -i 's/ISTART = 1/ISTART = 0/g' INCAR
            sed -i 's/ICHARG = 2/ICHARG = 1/g' INCAR
            cd ..
        fi
    done

    #inform the user that the INCAR has been updated
    echo "The INCAR file has been updated to restart the job(s)"

}

function sendFile {

    echo $(pwd)$1

}

# function clearDirectory {

#     # remove all files in the vasp directory other than the INCAR, POTCAR, KPOINTS and POSCAR files
#     echo "Clearing directory..."

#     ls | grep -v

# }

function trackSCF {
    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    i=1
    while read -r line; do
        if [[ $line =~ TOTEN ]]; then
            data=$(awk -v i="$i" '{print i, $(NF-1)}')
            echo "$data" >>scf.dat
            i=$((i + 1))
        fi
    done <"$outcar"

    echo "The scf.dat file has been created"
}

function submitJob {

    #submits a job to the queue with the name of the current directory

    #if $1 is empty, then alert the user that a submission script is required

    if [ -z "$1" ]; then
        echo "A submission script is required"
        exit
    fi

    qsub -N ${PWD##*/} $1
}

function duplicateDir {

    # $1 is the path of the directory to be copied
    # $2 is the name/path of the new directory
    # there is an optional flag to copy the POSCAR instead of the CONTCAR

    # check if the -p flag is set
    files=("KPOINTS" "INCAR" "POTCAR")
    if [[ "$1" == "-p" ]]; then
        cp "$2/POSCAR" "$3/"

        for file in "${files[@]}"; do
            cp "$2/$file" "$3/"
        done

    else

        cp "$1/CONTCAR" "$2/POSCAR"
        for file in "${files[@]}"; do
            cp "$1/$file" "$2/"
        done

        echo "NOTE: CONTCAR has been copied to the POSCAR in the new directory"
        echo "NOTE: If you would like to copy the POSCAR instead, use the -p flag"

    fi

}
