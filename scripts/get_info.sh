#!/bin/bash

data_file="data.csv"
echo JobType,Atoms,Energy,Electrons,Bands,NKpoints,Kx,Ky,Kz,Drift > "$data_file"


    #get the directory name and save as job_type
    job_type=$(basename "$PWD")
    #get the number of atoms
    atoms=$(grep "NIONS" OUTCAR | awk '{print $12}')
    #Get the final energy
    energy=$(grep "TOTEN" OUTCAR | tail -1 | awk '{print $5}')
    #Get the number of electrons
    electrons=$(grep "NELECT" OUTCAR | awk '{print $3}')
    #Get the number of bands
    bands=$(grep "NBANDS" OUTCAR | awk '{print $15}')
    #Get the number of k-points
    kpoints=$(grep "NKPTS" OUTCAR | awk '{print $4}')
    #Get the fourth line of the KPOINTS file
    k=$(sed -n '4p' KPOINTS)
    #Get the Kx, Ky, and Kz values
    kx=$(echo "$k" | awk '{print $1}')
    ky=$(echo "$k" | awk '{print $2}')
    kz=$(echo "$k" | awk '{print $3}')
    # Get the average drift of the x, y, and z components of the lattice vectors
    drift=$(grep "drift" OUTCAR | awk '{print $4, $5, $6}' | awk '{sum+=$1} END {print sum/NR}')
    #write information to $data_file.csv
    echo "$job_type,$atoms,$energy,$electrons,$bands,$kpoints,$kx,$ky,$kz,$drift" >> "$data_file"
