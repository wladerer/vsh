#!/bin/bash

#take structure file as input from command line
file=$( realpath "$1" )

for thickness in 2 4 6 8 10 12 14 16; do

    mkdir -p "t$thickness" ; cd "t$thickness" || exit

    vsh slab "$file" -m 0 0 1 -o slab -u -t $thickness


    vsh kpoints --mesh 9 9 1 -o KPOINTS
    vsh kpoints --plane 60 -o KPATH
    vsh incar --write slab -o geom.incar
    vsh incar --write band-slab -o band.incar
    vsh incar --write single-point-slab -o sod.incar
    vsh incar --write single-point-slab-soc -o soc.incar


    #for every .vasp file in the current directory, make a subdirectory
    #and copy the file into it

    for i in *.vasp; do
        dir="${i%.vasp}"
        mkdir -p "$dir"/band "$dir"/sod "$dir"/soc

        rsync -av --exclude='*.vasp' --exclude='KPOINTS' --exclude='KPATH' --exclude='*.incar' "$i" "$dir"/POSCAR
        rsync -av --exclude='KPATH' KPOINTS "$dir"
        rsync -av KPOINTS "$dir"/sod
        rsync -av KPOINTS "$dir"/soc
        rsync -av KPATH "$dir"/band

        #copy the INCAR files into the subdirectories
        rsync -av geom.incar "$dir"/INCAR
        rsync -av band.incar "$dir"/band/INCAR
        rsync -av sod.incar "$dir"/sod/INCAR
        rsync -av soc.incar "$dir"/soc/INCAR
        
    done

    cd .. || exit

done