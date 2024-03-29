# vsh

vsh is a command line utility for interacting with VASP. This is meant to simplify the numerous tools provided by libraries such as 
[pymatgen](https://pymatgen.org/), [ASE](https://wiki.fysik.dtu.dk/ase/), [pyprocar](https://romerogroup.github.io/pyprocar/), and others alike. 

To view formatted documentation, you may open `docs/vsh.html` in your browser. This can be done with command line on most Linux distros

```bash
xdg-open docs/vsh.html
```

or in MacOs

```bash
open docs/vsh.html
```
___

### Usage

vsh comes with several modules meant to assist in the preperation and analysis of VASP calculations. To see all of the possible modules, invoke the '-h' flag 
to see what is available

```
vsh -h
```

### Features

vsh is currently equipped with a wide range of tools. Most notably, vsh has utilities to prepare band structure calculations, generate slabs, and handle detailed ASE databases. Invoke either `vsh incar -h`, `vsh slab -h`, or `vsh db -h` to learn more about their functionality. 

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

##### band

band is a glorified wrapper for [pyprocar](https://romerogroup.github.io/pyprocar/) with only an additional input parser to simplify plotting. Adjustments have been made to the default behavior - namely preference for the parametric plotting mode instead of the 'plain' mode. Additional quality of life features have been included as well - such as specifying the orbitals by symbol rather than arbitrary number.

##### db

vsh contains a wrapper for the ASE database utility. There have been some adjustments to the default ASE database behavior to include more information regarding the initial parameters and results of a VASP calculation. 

##### slab

slabgen is a module intended to simplify the process of making slabs of bulk materials. Many options are included in the specification of typical parameters such as vacuum, slab thickness, and miller plane. 

##### incar, poscar, potcar, and kpoints

These four modules handle the creation and modification of their respective files. Notably, `kpoints` can handle any type of KPOINTS file and can even produce high-symmetry k-paths from the SeekPath API. 

`poscar` is able to convert and manipulate any file type containing structural information. You are also able to create molecules surrounded by vacuum to perform molecular calculations in VASP.

Additionally, there is a static surface projected band path that follows $M - K - \Gamma - M$. 

##### wavecar

Convert WAVECARS to cube, parchg, and Wannier90 $U_{nk}$ files. You can also project coefficients onto a 3D fft mesh grid. 

##### procar

procar is quite a built out utility with many options, so please refer to the -h output. Procar does orbital and compositonal analyses on a band and kpoint basis. You can also plot and query these properties. It is recommended that you pickle your vasprun.xml file prior to using the utility to save time. Additionally, the procar module is able to plot interactive band structures for quick reference (not publication ready figures)

##### cohp

This module is inteded to plot COHPs produced by the [LOBSTER](http://www.cohp.de/) program. You are able to plot multiple directories at a time. 




