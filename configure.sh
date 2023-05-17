#!/bin/bash

#check if the VSHDIR variable is set
if [ -z "$VSHDIR" ]; then
    echo "VSHDIR is not set"
    
    #prompt the user to set the VSHDIR variable
    echo "Please set the VSHDIR variable to the directory where you have cloned the vsh repository"
    exit
fi

#checks to see if ~/.bashrc sources vsh/v.sh and vsh/.vshrc and if not, adds them
if ! grep -q "source $VSHDIR/v.sh" ~/.bashrc; then
    echo "source $VSHDIR/v.sh" >>~/.bashrc
fi

if ! grep -q "source $VSHDIR/.vshrc" ~/.bashrc; then
    echo "source $VSHDIR/.vshrc" >>~/.bashrc
fi

if ! grep -q "source $VSHDIR/bin" ~/.bashrc; then
    echo "source $VSHDIR/bin" >>~/.bashrc
fi



#source the .bashrc file
source ~/.bashrc



