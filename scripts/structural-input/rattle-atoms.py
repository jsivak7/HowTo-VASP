"""
JTSivak 07.08.2022

Description
-----------
Randomly displace atoms within a structure file that is supported by Atomic Simulation Environment (ASE). I commonly used this for mixed metal TMO systems (especially those with a local distortions such as the rocksalt CuO Jahn-Teller distortion of the local octahedra). While it can make relaxation take longer, I think that this is worthwhile to break the cubic symmetry since this can lead to falling into local minima states where the minimization algorithms cannot escape from these minima. I also believe (I don't really have proof at the moment), that this should help with removing the potential for ordering of these distortions. For a "truly random structure", you wouldn't necessarily want this, however it may be a of interest, so be sure to logically think about whether or not you want to use this. As always TEST THINGS, since I believe this is one of the only ways to go about complex calculations like these.
-----------

To run
------
$ python rattle-atoms.py STRUCTURE.file STD_DEV
------

Advice/Notes to Myself
----------------------
- I am using a STD_DEV of 0.05 currently as 0.1 seemed like too large of distortions, but 0.01 was too small to really make the desired difference I think.
----------------------

"""

from ase import Atoms
from sys import argv
from ase.io import read,write
import random

# these are user inputs defined in in command line
file = argv[1] # structural file which we want to rattle the atoms of
rattle_amount = float(argv[2]) # amount which we want to random displace the atoms in our structure

# where the actual work gets done 
atoms = read(file) # read in OG file
atoms.rattle(rattle_amount, seed = int(random.uniform(0, 2000))) # actually perform the rattle operation on the system
    # the random numbers are drawn from a normal distribution of standard deviation "rattle_amount"
write(file, atoms) # output new rattled structure to same file