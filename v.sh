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
    grep E-fermi $outcar | tail -1 | awk -F " " '{print $3}'
}

function getElements {

    # if $1 is empty, then assume $1=./OUTCAR
    poscar=${1:-./POSCAR}

    # combine the two lines to get the element list
    sed -n 6p $poscar | awk -F " " '{print $0}' && sed -n 7p $poscar | awk -F " " '{print $0}'

}

function getKx {

    # if $1 is empty, then assume $1=./KPOINTS
    kpoints=${1:-./KPOINTS}

    #check if 3rd line of the KPOINTS file is Recirprocal or reciprocal, if so return Null
    if [[ $(sed -n 3p $kpoints) == *"Reciprocal"* ]]; then
        echo "Null"
    else
    #fourth line of the KPOINTS file
    sed -n 4p $kpoints | awk -F " " '{print $1}'
    fi



}

function getKy {

    # if $1 is empty, then assume $1=./KPOINTS
    kpoints=${1:-./KPOINTS}

       #check if 3rd line of the KPOINTS file is Recirprocal or reciprocal, if so return Null
    if [[ $(sed -n 3p $kpoints) == *"Reciprocal"* ]]; then
        echo "Null"
    else
    #fourth line of the KPOINTS file
    sed -n 4p $kpoints | awk -F " " '{print $2}'
    fi


}

function getKz {

    # if $1 is empty, then assume $1=./KPOINTS
    kpoints=${1:-./KPOINTS}

    #check if 3rd line of the KPOINTS file is Recirprocal or reciprocal, if so return Null
    if [[ $(sed -n 3p $kpoints) == *"Reciprocal"* ]]; then
        echo "Null"
    else
    #fourth line of the KPOINTS file
    sed -n 4p $kpoints | awk -F " " '{print $3}'
    fi

}


function getESteps {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    grep -c 'Iteration' "$outcar"

}

function getISteps {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    grep -a Iteration "$outcar" | tail -1 | awk '{print $3}' | tr -d '('
}

function getDriftx {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    grep -a drift "$outcar" | tail -1 | awk '{print $3}'

}

function getDrifty {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    grep -a drift "$outcar" | tail -1 | awk '{print $4}'

}

function getDriftz {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    grep -a drift "$outcar" | tail -1 | awk '{print $5}'

}


function getEdiffg {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    grep -a EDIFFG "$outcar" | tail -1 | awk '{print $3}'

}

function getEdiff {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    grep -a EDIFF "$outcar" | head -n 1 | awk '{print $3}'

}

function getEncut {

    # if $1 is empty, then assume $1=./OUTCAR
    outcar=${1:-./OUTCAR}

    grep -a ENCUT "$outcar" | head -n 1 | awk '{print $3}'

}

function updateTag {

    # check if the $1 or $2 variables are the incar file
    # if so, then inform the user that the order of arguments is $1 = tag, $2 = value, $3 = incar file
    #check for the substring INCAR in the whole string

    if [[ "$1" == *"INCAR"* ]]; then
        echo "The order of arguments is \n updateTag tag value INCAR_file"
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
            cd "$dir" 
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

    echo $(pwd)/$1

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

        #if the difference is positive, print an arrow pointing up and vice versa, if the difference is 0 then print a horizontal line
        if (($(echo "$diff > 0" | bc -l))); then
            echo -e "$i \e[32m▲\e[0m"
        elif (($(echo "$diff < 0" | bc -l))); then
            echo -e "$i \e[31m▼\e[0m"
        else
            echo -e "$i \e[34m─\e[0m"
        fi

    done

}

function submitJob {

    #submits a job to the queue with the name of the current directory

    #if $1 is empty, then alert the user that a submission script is required

    if [ -z "$1" ]; then
        echo "A submission script is required"
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

    echo "Number of steps: $(grep -c 'Iteration' $outcar)"
    echo "Ionic Steps: $(grep -a Iteration OUTCAR | tail -1 | awk '{print $3}' | tr -d '(' )"
    echo "Final Energy: $(grep -a TOTEN $outcar | tail -1 | awk '{print $5}')" \(eV\)
    echo "Total Drift (x, y, z): $(grep -a drift $outcar | tail -1 | awk '{print $3 , $4 , $5}' )" 
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

function createIncar {

    # These are the default env variables found in the .vshrc file
    #  INCAR_BULK_GEOPT_LOW
    #  INCAR_BULK_GEOPT_MED
    #  INCAR_BULK_GEOPT_HIGH
    #  INCAR_SLAB_GEOPT_LOW
    #  INCAR_SLAB_GEOPT_MED
    #  INCAR_SLAB_GEOPT_HIGH
    #  INCAR_SPIN_ORBIT
    #  INCAR_BAND_STRUCTURE

    if [ $# -lt 1 ]; then
        echo "Usage: createIncar [-b|-s] [low|med|high]"
        return 1
    fi

    if [ "$1" == "-b" ]; then
        if [ "$2" == "low" ]; then
            cp "$INCAR_BULK_GEOPT_LOW" INCAR
        elif [ "$2" == "med" ]; then
            cp "$INCAR_BULK_GEOPT_MED" INCAR
        elif [ "$2" == "high" ]; then
            cp "$INCAR_BULK_GEOPT_HIGH" INCAR
        else
            cp "$INCAR_BULK_GEOPT_MED" INCAR
        fi
    elif [ "$1" == "-s" ]; then
        if [ "$2" == "low" ]; then
            cp "$INCAR_SLAB_GEOPT_LOW" INCAR
        elif [ "$2" == "med" ]; then
            cp "$INCAR_SLAB_GEOPT_MED" INCAR
        elif [ "$2" == "high" ]; then
            cp "$INCAR_SLAB_GEOPT_HIGH" INCAR
        else
            cp "$INCAR_SLAB_GEOPT_MED" INCAR
        fi
    else
        echo "Usage: createIncar [-b|-s] [low|med|high]"
        return 1
    fi

}

function validateIncar {

    # $1 is the path to the INCAR file, if $1 is empty, then assume $1=./INCAR
    incar=${1:-./INCAR}
    #checks if each INCAR tag exists in $VSHDIR/incar_tags.txt
    #if it does not, then it is printed to the screen

    #check if the INCAR file exists
    if [ ! -f "$incar" ]; then
        echo "INCAR file not found"
        return 1
    fi

    #check if the incar_tags.txt file exists
    if [ ! -f "$VSHDIR/incar_tags.txt" ]; then
        echo "incar_tags.txt file not found"
        return 1
    fi

    #check if the incar_tags.txt file is empty
    if [ ! -s "$VSHDIR/incar_tags.txt" ]; then
        echo "incar_tags.txt file is empty"
        return 1
    fi

    #check if the INCAR file is empty
    if [ ! -s "$incar" ]; then
        echo "INCAR file is empty"
        return 1
    fi

    #check if each tag in the INCAR file is in the incar_tags.txt file
    while read tag; do
        if ! grep -q "$tag" "$incar"; then
            echo "$tag not found in INCAR file"
        fi
    done <"$VSHDIR/incar_tags.txt"

}

function testKpoints {

    #takes a directory, $1, and pulls the kpoints from the KPOINTS file
    #number of new directories to create, $2
    #increments the kpoints by $3
    #creates a new directory with new kpoints and adds existing INCAR, POTCAR, and POSCAR to the new directories 

    #check if $1 is a directory, if not, assume current directory
    if [ ! -d "$1" ]; then
        echo "Directory not found"
        echo "Usage: testKpoints directory number_of_directories increment"
        return 1
    fi

    #check if $2 is a number, if not, assume 1

    if ! [[ "$2" =~ ^[0-9]+$ ]]; then
        echo "Not a number"
        echo "Usage: testKpoints directory number_of_directories increment"
        return 1
    fi

    #check if $1/KPOINTS exists

    if [ ! -f "$1/KPOINTS" ]; then
        echo "KPOINTS file not found"
        return 1
    fi

    #get the kpoints from the KPOINTS file
    kpoints=$(cat $1/KPOINTS | head -n 4 | tail -1 | awk '{print $1, $2, $3}')
    k_x=$(echo $kpoints | awk '{print $1}')
    k_y=$(echo $kpoints | awk '{print $2}')
    k_z=$(echo $kpoints | awk '{print $3}')

    #check if $3 is a number, if not, assume 3

    if ! [[ "$3" =~ ^[0-9]+$ ]]; then
        echo "Not a number"
        echo "Usage: testKpoints directory number_of_directories increment"
        return 1
    fi

    #create the new directories

    for ((i = 1; i <= $2; i++)); do
        mkdir "$1/kpoints_$i"
        cp "$1/INCAR" "$1/kpoints_$i"
        cp "$1/POTCAR" "$1/kpoints_$i"
        cp "$1/POSCAR" "$1/kpoints_$i"
        echo "Kpoint Testing File" >"$1/kpoints_$i/KPOINTS"
        echo "0" >>"$1/kpoints_$i/KPOINTS"
        echo "Gamma" >>"$1/kpoints_$i/KPOINTS"
        echo "$kpoints" >>"$1/kpoints_$i/KPOINTS"

        k_x=$((k_x + $3))
        k_y=$((k_y + $3))
        k_z=$((k_z + $3))

        kpoints="$k_x $k_y $k_z"

    done
    

}

function addTag {

    # $1 is the INCAR file, if $1 is empty, then assume $1=./INCAR
    incar=${1:-./INCAR}
    # $2 is the tag to add
    tag=$2
    # $3 is the value of the tag to add
    value=$3

    #check if the INCAR file exists
    if [ ! -f "$incar" ]; then
        echo "INCAR file not found"
        return 1
    fi

    line="$tag = $value"

    #check if the tag already exists in the INCAR file
    if grep -q "$tag" "$incar"; then
        echo "Tag already exists in INCAR file"
        return 1
    fi

    #update the INCAR file
    echo "$line" >>"$incar"

}

function removeTag {

    # $1 is the INCAR file, if $1 is empty, then assume $1=./INCAR
    incar=${1:-./INCAR}
    # $2 is the tag to remove
    tag=$2

    #check if the first argument is a file
    if [ ! -f "$1" ]; then
        echo "First argument is not a file"
        return 1
    fi


    #check if the tag exists in the INCAR file
    if ! grep -q "$tag" "$incar"; then
        echo "Tag not found in INCAR file"
        return 1
    fi

    #remove the tag from the INCAR file
    sed -i "/$tag/d" "$incar"

}

function estimateBands {

    # extract the number of atoms in the unit cell
    NATOMS=$(sed -n '7p' POSCAR | awk '{sum=0; for (i=1; i<=NF; i++) {sum+=$i}} END {print sum}')

    # extract the number of k-points from the KPOINTS file
    NKPTS=$(sed -n '4p' KPOINTS | awk '{product=1; for (i=1; i<=NF; i++) {product*=$i}} END {print product}')

    # extract the number of electrons per atom from the POTCAR file
    NEL=$(grep "TITEL" POTCAR | awk '{sum=0; for (i=5; i<=NF; i++) {sum+=$i}} END {print sum}')

    # estimate the total number of electrons
    NEL_TOT=$(echo "$NEL * $NATOMS" | bc -l)

    # estimate the number of bands
    NBANDS=$(echo "$NEL_TOT * $NKPTS / $NATOMS" | bc -l)

    # vasp recommended number of bands (NELECT + NIONS) / 2
    NBANDS_REC=$(echo "$(($NEL_TOT/2 + $NATOMS/2))" | bc -l)

    echo "Estimated number of bands (kpoint  method): $NBANDS"
    echo "Recommended number of bands (NELECT + NIONS) / 2: $NBANDS_REC"
  

}

function recommendPerformanceTags {

    directory=$1
    CORES_PER_NODE=$2

    #check if INCAR, POSCAR, and KPOINTS files exist
    if [ ! -f "$directory/INCAR" ]; then
        echo "INCAR file not found"
        return 1
    fi

    if [ ! -f "$directory/POSCAR" ]; then
        echo "POSCAR file not found"
        return 1
    fi

    if [ ! -f "$directory/KPOINTS" ]; then
        echo "KPOINTS file not found"
        return 1
    fi

    #check if the number of cores per node is a number
    if ! [[ "$CORES_PER_NODE" =~ ^[0-9]+$ ]]; then
        echo "Not a number"
        return 1
    fi

    # VASP recommends 1 core per atom, 4-8 bands per core, KPAR = nodes

    NBANDS=$(estimateBands)

    #extract the number of atoms in the unit cell
    NATOMS=$(sed -n '7p' $directory/POSCAR | awk '{sum=0; for (i=1; i<=NF; i++) {sum+=$i}} END {print sum}')

    #extract the number of k-points from the KPOINTS file
    NKPTS=$(sed -n '4p' $directory/KPOINTS | awk '{product=1; for (i=1; i<=NF; i++) {product*=$i}} END {print product}')

    echo "Recommended tags:"
    echo "NPAR = $CORES_PER_NODE"
    echo "NBANDS = $NBANDS"
    echo "KPAR = $CORES_PER_NODE"

}


function tabulateResults {

    #$1 is the directory to search for vasp files
    directory=$1

    #$2 is the file to write the results to
    
    #check if the directory exists
    if [ ! -d "$directory" ]; then
        echo "Directory not found"
        return 1
    fi

    #check if the directory contains vasp files
    if [ ! -f "$directory/OUTCAR" ]; then
        echo "OUTCAR file not found"
        return 1
    fi
    outcar="$directory/OUTCAR"

    atom_types=$(sed -n '6p' "$directory"/POSCAR)
    natoms=$(sed -n '7p' "$directory"/POSCAR | awk '{sum=0; for (i=1; i<=NF; i++) {sum+=$i}} END {print sum}')
    kpoints=$(sed -n '4p' "$directory"/KPOINTS | awk '{product=1; for (i=1; i<=NF; i++) {product*=$i}} END {print product}')
    energy=$(grep "energy  without entropy" "$directory"/OUTCAR | tail -1 | awk '{print $NF}')
    scf_steps=$(grep -c 'Iteration' "$directory/OUTCAR")
    ionic_steps=$(grep -a Iteration "$directory/OUTCAR" | tail -1 | awk '{print $3}' | tr -d '(' )
    final_energy="$(grep -a TOTEN "$outcar" | tail -1 | awk '{print $5}')"
    drift_x=$(grep -a drift "$outcar" | tail -1 | awk '{print $3}' )
    drift_y=$(grep -a drift "$outcar" | tail -1 | awk '{print $4}' ) 
    drift_z=$(grep -a drift "$outcar" | tail -1 | awk '{print $5}' )
    path=$(pwd)
    #create a header if the file does not exist
    if [ ! -f "$2" ]; then
        echo "atom_types,natoms,kpoints,energy,scf_steps,ionic_steps,final_energy,drift_x,drift_y,drift_z,path" >"$2"
    fi

    #write the results to the file
    echo "$atom_types,$natoms,$kpoints,$energy,$scf_steps,$ionic_steps,$final_energy,$drift_x,$drift_y,$drift_z,$path" >>"$2" 

}


function updateDatabase {
	#get the user database file from the environment variable $VSHDB
	dbfile=$VSHDB

	#check if the database file exists
	if [ ! -f "$dbfile" ]; then
		echo "Database file not found"
		return 1
	fi

	#use the tabulateResults function to update the database
	tabulateResults "$1" "$dbfile"
	
	#notify the user that the database has been updated
	echo "Database updated"

}
