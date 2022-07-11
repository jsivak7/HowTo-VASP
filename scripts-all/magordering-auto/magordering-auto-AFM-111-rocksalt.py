"""
JTSivak 07.11.2022

Description
-----------
This can be used to automatically generate a user-defined magnetic ordering for a VASP (or probably any other electronic structure code). This current script is for the 2x2x2 supercell of a rocksalt oxide which is 64 atoms. I will outline how to change this for different crystal structures or different sized supercells as well.

This should work for point defects within the inputted structure as well, although I have not tested it just yet

NOTE be sure that you use the EXACT file which will be used in the calculation since the .cif/.xyz/etc. file will have a different atomic numbering scheme than the POSCAR/structural file that is inputted into the electronic structure calculation.

NOTE that within ASE (and more specifically Python), that the atomic coordinates begin at 0 rather than 1
-----------

To run
------
$ python magordering-auto-AFM-111-rocksalt.py
------

To Modify
---------
NEED TO DO STILL
---------

To Do
----------------------
- add example
- make this go over many different directories so that it can be used better for high throughput calculations without needed to go in and out of directories yourself
- make this so atoms are given a magnetic moment based on their element type
- make more scripts for different supercell sizes for the rocksalt oxide
----------------------

"""

from ase import Atoms
from ase.io import read, write
import numpy as np
import subprocess

s = read("NiO_POSCAR") # structural file which we want to get the magnetic ordering for
    # NOTE that this MUST be the pristine crystal lattice - any distortions or rattling of the atomic coordinates should be done after this

a = 4.211 # this is the lattice parameter for the crystal structure
    # NOTE that this currently is only implemented for cubic rocksalt lattice

magnetic_moment = 2 # the magnetic moment which we want to add to all magnetic atoms

coords = s.get_positions() # this gets all of the atomic coordinates within the inputted structure in Cartesian coordinates

# this is where the atomic coordinates which should be either spin-up or spin-down are located
# NOTE that the user will need to change these for every different crystal structure and magnetic ordering
#--------------------------------------
spin_up = np.array([ 
                [0, 0, 0], 
                [0, a/2, a*1.5], 
                [a/2, 0, a*1.5], 
                [a/2, a/2, a], 
                [0, a*1.5, a/2], 
                [a/2, a, a/2], 
                [a/2, a*1.5, 0], 
                [0, a, a], 
                [a, a/2, a/2], 
                [a*1.5, 0, a/2], 
                [a*1.5, a/2, 0.0], 
                [a, 0, a], 
                [a, a, 0], 
                [a, a*1.5, a*1.5], 
                [a*1.5, a, a*1.5], 
                [a*1.5, a*1.5, a]
                ])

spin_down = np.array([ 
                [0, a/2, a/2], 
                [a/2, 0, a/2], 
                [a/2, a/2, 0], 
                [0, 0, a], 
                [0, a, 0], 
                [0, a*1.5, a*1.5], 
                [a/2, a, a*1.5], 
                [a/2, a*1.5, a], 
                [a, 0, 0], 
                [a, a/2, a*1.5], 
                [a*1.5, 0, a*1.5], 
                [a*1.5, a/2, a], 
                [a, a*1.5, a/2], 
                [a*1.5, a, a/2], 
                [a*1.5, a*1.5, 0], 
                [a, a, a] ])
#--------------------------------------


# define the lists which will contain the atomic numbers which should be either spin up or spin down
# these will be filled in based on the arrays defined above by the user which specify which atomic coordinates should be either spin-up or spin-down
up_index = []
down_index = []

# loops for going over all of the atomic coordinates within the inputted structure to determine if they should be spin-up or spin-down
# this is based on the arrays defined above (spin_up and spin_down)
for i in range(len(coords)):
    for j in range(len(spin_up)): # NOTE that this needs to be an equal amount of spin up and down with the current implementation...
        if np.array_equal(spin_up[j], coords[i]) == True: # this tests for if the atomic coordinates match what the user defines for a spin-up atom
            up_index.append(i) # if it matches, then append the atom number to the up_index list
        elif np.array_equal(spin_down[j], coords[i]) == True: # this tests for if the atomic coordinates match what the user defines for a spin-up atom
            down_index.append(i) # if it matches, then append the atom number to the down_index list

# define list for the final magnetic moments in the same order as the inputted structure such that it can be added to the INCAR (or whatever input structure)
magmom = []

# loop for creating a list that will correspond to the final MAGMOM tag that is added to the INCAR file
for i in range(len(coords)): # loops through all of the atomic numbers within the inputted structure
    if i in up_index:
        magmom.append(+magnetic_moment)
    elif i in down_index:
        magmom.append(-magnetic_moment)
    else:
        magmom.append(0)

# write the magmom list (the actual magnetic ordering) to a temporary file "tmp_ORDER.txt"
with open("tmp_ORDER.txt", "w") as output:
    output.write(str(magmom))

# run the bash script to add the magnetic ordering to the INCAR file within the same directory in the proper format
subprocess.run(["bash clean_up_magmom.sh"], shell = True)

# remove any of the tmp* files that were generated
subprocess.run(["rm tmp*"], shell = True)