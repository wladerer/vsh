# vsh

vsh is a command line utility for interacting with VASP. This is meant to simplify the numerous tools provided by libraries such as 
[pymatgen](https://pymatgen.org/), [ASE](https://wiki.fysik.dtu.dk/ase/), [pyprocar](https://romerogroup.github.io/pyprocar/), and others alike. 
___

### Usage

vsh comes with several modules meant to assist in the preperation and analysis of VASP calculations. To see all of the possible modules, invoke the '-h' flag 
to see what is available

```
vsh -h
```

### Features

vsh is currently equipped with a wide range of tools. Most notably, vsh has utilities to prepare band structure calculations, generate slabs, and handle detailed ASE databases. Invoke either `vsh inputs -h`, `vsh slabgen -h`, or `vsh db -h` to learn more about their functionality. 

#### Modules

The repository is separated into several modules to compartmentalize the various needs of a computational scientist.  
___
##### analysis

 Analysis is intended to quickly read data from the OUTCAR and vasprun.xml files produced by VASP. This is by no means a replacement for going over the data yourself - simply a tool to check on the status of a calculation and get a quick glance at the raw output. 

 The most reqularly used utility is checking the ionic and electronic convergence of a VASP calculation. 

 ```bash
 vsh analysis --converged
 ```

 This can be used in combination with other shell commands to become a powerful organizational tool. For example, the following code block is a one-liner that does a recursive search for all directories containing `vasprun.xml` and checks to see if the calculation has converged. 

 ```bash 
shopt -s globstar; for dir in /path/to/search/**/; do [ -f "$dir/vasprun.xml" ] && (cd "$dir" && vsh analysis --converged); done
 ```

##### bands

bands is a glorified wrapper for [pyprocar](https://romerogroup.github.io/pyprocar/) with only an additional input parser to simplify plotting. Adjustments have been made to the default behavior - namely preference for the parametric plotting mode instead of the 'plain' mode. 

##### db

vsh contains a wrapper for the ASE database utility. There have been some adjustments to the default ASE database behavior to include more information regarding the initial parameters and results of a VASP calculation. 

##### freeze

This is soon to be deprecated and moved into the `inputs` module. 

##### slab

slabgen is a module intended to simplify the process of making slabs of bulk materials. Many options are included in the specification of typical parameters such as vacuum, slab thickness, and miller plane. 

##### inputs

inputs currently handles the creation and manipulation of multiple kinds of VASP input files. 

Note: Pseudopotentials must be configured using the `pmg config` command provided by pymatgen. 

##### manage

A simple utility to help archive job output or duplicate job inputs. 





