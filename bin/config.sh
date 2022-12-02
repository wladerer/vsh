#!/bin/bash

#This is a script to help configure your ~/.vshrc file. 
#For now, it is used as a list of file types or filenames to ignore when archiving. 
#In the future, it will be used to configure more settings and improve functionalitly

dirpath=~/.vshrc
mkdir $dirpath
touch ${dirpath}/vshIgnore
touch ${dirpath}/relax
touch ${dirpath}/spin_orbit
touch ${dirpath}/band

