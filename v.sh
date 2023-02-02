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

function getNatoms {

    #if $1 is empty, then assume $1=./

    if [ -z "$1" ]; then
        outcar=./OUTCAR
    else
        outcar=$1
    fi
    grep NIONS $outcar | awk -F " " '{print $NF}'
}

function getEfermi {

    #if $1 is empty, then assume $1=./

    if [ -z "$1" ]; then
        outcar=./OUTCAR
    else
        outcar=$1
    fi
    grep E-fermi $outcar | awk -F " " '{print $NF}'
}

function getElements {

    # if $1 is empty, then assume $1=./OUTCAR
    poscar=${1:-./POSCAR}

    # combine the two lines to get the element list
    sed -n 6p $poscar | awk -F " " '{print $0}' && sed -n 7p $poscar | awk -F " " '{print $0}'

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


function trackSCF {
    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}
    #get the number of SCF cycles
    nscf=$(grep -c "TOTEN" $outcar)

    #use nscf as a counter for the rows
    for ((i = 1; i <= nscf; i++)); do
        #get the energy for each SCF cycle
        energy=$(grep -m $i "TOTEN" $outcar | tail -n 1 | awk -F " " '{print $(NF-1)}')
        #add the iteration number and energy to the scf.dat file
        echo "$i $energy" >>scf.dat

        #upate a progress bar
        echo -ne "SCF cycles completed: $i/$nscf\r"

    done

    echo "The scf.dat file has been created"
}

function visualizeSCF {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    # if scf step i+1 - step i is + , print i+1 spaces, \ , and a new line
    # if scf step i+1 - step i is - , print i-1 spaces, / , and a new line 
    # if scf step i+1 - step i is 0 , print i spaces, - , and a new line


    #get the number of SCF cycles
    nscf=$(grep -c "TOTEN" $outcar)

    #use nscf as a counter for the rows
    for ((i = 1; i <= nscf; i++)); do

        #skip the first and last SCF cycles
        if [[ $i -eq 1 ]] || [[ $i -eq $nscf ]]; then
            continue
        fi

        #get the energy for each SCF cycle
        energy=$(grep -m $i "TOTEN" $outcar | tail -n 1 | awk -F " " '{print $(NF-1)}')

        #get the energy for the previous SCF cycle
        prev_energy=$(grep -m $((i - 1)) "TOTEN" $outcar | tail -n 1 | awk -F " " '{print $(NF-1)}')

        #get the difference between the current and previous SCF cycles
        diff=$(echo "$energy - $prev_energy" | bc)

        #if the difference is positive, print a backslash
        if (( $(echo "$diff > 0" | bc -l) )); then
            
            #print the number of spaces equal to the current SCF cycle and a backslash
            printf "%${i}s\\

" ""

        #if the difference is negative, print a forward slash
        elif (( $(echo "$diff < 0" | bc -l) )); then

            #print the number of spaces equal to the current SCF cycle and a forward slash
            printf "%${i}s/

" ""
    
            #if the difference is zero, print a dash
            else
    
                #print the number of spaces equal to the current SCF cycle and a dash
                printf "%${i}s-- 
                " ""


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

function summarizeOutcar {
    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    echo "Number of ionic steps: $(grep -c 'Iteration' $outcar)"
    echo "Final energy (eV): $(grep 'FREE ENERGIE' $outcar | tail -1 | awk '{print $5}')"
    echo "Final total energy (eV): $(grep 'TOTAL ENERGIE' $outcar | tail -1 | awk '{print $4}')"
    echo "Final total charge (e): $(grep 'number of electrons' $outcar | tail -1 | awk '{print $8}')"
}

function createKpoints {
    mode=gamma
    while [ $# -gt 0 ]; do
        case "$1" in
        -m)
            mode=mesh
            ;;
        *)
            break
            ;;
        esac
        shift
    done

    if [ $# -ne 3 ]; then
        echo "Usage: createKpoints [-m] k_x k_y k_z"
        return 1
    fi

    k_x=$1
    k_y=$2
    k_z=$3

    echo "Automatic mesh" >kpoints.vsh
    echo "$mode" >>kpoints.vsh
    echo "0" >>kpoints.vsh
    echo "$k_x $k_y $k_z" >>kpoints.vsh
    echo "0 0 0" >>kpoints.vsh

}

function createPotcar {

    if [ -z "$VASP_POTENTIAL_DIRECTORY" ]; then
        echo "VASP_POTENTIAL_DIRECTORY is not set."
        return 1
    fi

    if [ $# -lt 1 ]; then
        echo "Usage: createPOTCAR atom1 [atom2 ...]"
        return 1
    fi

    for atom in "$@"; do
        potcar="$VASP_POTENTIAL_DIRECTORY/$atom/POTCAR"
        if [ ! -f "$potcar" ]; then
            echo "POTCAR for $atom not found."
            return 1
        fi
        cat "$potcar" >>POTCAR

    done
}
