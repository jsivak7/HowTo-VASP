# HowTo-VASP
A collection of my experience with VASP for performing DFT calculations on transition metal oxide systems, including tips and tricks as well as some examples.

## Random notes
- need to make sure that you have your .pmgrc file set up correctly with the VASP PAW potentials in order to use the make_vasp*.py files
    - add in an example of how to do this (or at least hyperlink to pmg website on how to set this up properly)

## To Do
- add in convergence testing examples
- add in Pulay stress example
- add images of how to more quickly do the magnetic ordering for the POSCAR file once the VASP files are generated
- showing how important initial guesses are for DFT calculations going to local minima
- examples of differences for ALGO = Fast/Normal/All for complex systems
- example of need for increasing NBANDS in calculation
- start adding in scripts for analysis stuff
    - density of states
    - local environment (w.r.t vacancies and changes)