"""
JTSivak 07.10.2022

Description
-----------
This is for generating all of the VASP input files for a calculation to be run on the Penn State ROAR system. I find that using this helps for more automation in getting these calculations set up and helps so that we make less human mistakes that without automation. NOTE that I explicitly define alot of different tags (which I would recommend to ensure you are using the parameters that you think you are), but one technically could get rid of alot of these if they wanted.

NOTE that there are some tags which need to be specified by the user, so these just currently have placeholders (in all CAPS)
-----------

To run
------
$ python make_vasp_fullrelax.py
------

"""

from pymatgen.io.vasp.sets import MPRelaxSet
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.core import structure
from subprocess import call
from ase.io import read,write
import numpy as np
import os
import glob
# read in the structure you want to make VASP inputs for
struct = read('INPUT_STRUCTURE')

# nomenclature for files
name = 'NAME_FILES' # this is for the file where vasp files will be placed
abbrev_name = 'NAME_RUN' # this is for the qsub submission to ACI

# conversion of objects
atoms = struct.copy()
s = AseAtomsAdaptor.get_structure(atoms)

# this is where the user is able to change/delete/add different parameters for the VASP calculation being set up
# --------------------------------------------------------------------------------------------------------------
custom_setting = {
            'LDAU': True, # want to use hubbard U parameters
            'LDAUTYPE': 2, # using the dudarev approach where U(#)-J(0.0)
            'LDAUPRINT': 1, # write the occupancy matrix to the OUTCAR
            'LMAXMIX': 4, # recommended for d-electrons by the VASP Wiki
            'LDAUU': {'O':{'Mg':0, 'Co':4, 'Cu':5, 'Ni':5, 'Zn':0, 'Cr':4, 'Mn':4}}, # the Hubbard U value that is applied to the different elements
                # these are from the fittings which I have done, so you can change these if you want to use them for your own systems
            'LDAUJ': {'O':{'Mg':0, 'Co':0, 'Cu':0, 'Ni':0, 'Zn':0, 'Cr':0, 'Mn':0}}, # the Hubbard J value that is applied, but since we are using Dudarev approach this should ALWAYS be 0.0
            'LDAUL': {'O':{'Mg':0, 'Co':2, 'Cu':2, 'Ni':2, 'Zn':0, 'Cr':2, 'Mn':2}}, # to specify that we are applying the hubbard U correction the d orbitals
            'NSW': 100, # max number of ionic steps
            'ISMEAR': 0, # Gaussian smearing
            'ENCUT': 600, # using 600eV to eliminate Pulay stress
            'EDIFF': 1e-5, # energy convergence criteria within a single ionic step -- this seems to be a good average of speed and stringency in my experience
	        'EDIFFG': -0.010, # force convergence to less than 10 meV/angstrom
            'IBRION': 2, # using conjugate gradient ionic relaxation
            'NCORE': 1, # parallelization scheme
            'NELM': 500, # max number of electronic steps performed in the single scf loop
                # this is probably overkill, but for some of the HEOs it it necessary since they are very slow to converge
            'SIGMA': 0.05, # converged smearing value -- pretty small and suggested by VASP wiki
            'LCHARG': False, # writing the chgcar with the charge density 
            'LWAVE': False, # writing the wavecar with the wavefunctions
            'ALGO': 'All', # conjugate gradient electronic minimization algorithm -- seen better performance for my TMO structures
	        'ISIF': 3, # allow ionic positions to be relaxed as well as the cell
            'LASPH': True, # include non-spherical contributions related to the gradient of the density in the PAW spheres (recommended for d-elements)
            'LORBIT': 11, # to write the DOSCAR and Im-decomposed PROCAR
            'LREAL': 'Auto', # can have some small error in total energy, but greatly increases speed for larger structures
            'GGA': 'PS', # for using PBEsol XC functional 
            'ISYM': 0 # turn off all symmetry
                }
kpoints = {"reciprocal_density": 75} # should be a gamma centered 3x3x3 kpoint mesh for the 2x2x2 supercell of NiO (64 atoms)
# --------------------------------------------------------------------------------------------------------------

# this is for collecting all of the above specified parameter 
relax = MPRelaxSet(s, user_kpoints_settings = kpoints, user_incar_settings = custom_setting, force_gamma = True)

relax.write_input(name,include_cif=True) # writing the outputs themselves for VASP, as well as a .cif file of the inputted structure

# everything below is for writing the *run* file for whatever system you are working on to the submit the job
# -----------------------------------------------------------------------------------------------------------
os.chdir(name)

with open('runvasp_rhel7','w') as write_pbs:
    pbs = '''#!/bin/sh
    #PBS -N %s
    #PBS -r n
    #PBS -e scheduler.err
    #PBS -o scheduler.out
    #PBS -l walltime=12:00:00
    #PBS -l pmem=5000mb
    #PBS -l nodes=1:ppn=20
    #PBS -A open
    #PBS -l feature=rhel7

    cd $PBS_O_WORKDIR
    module purge
    module use /gpfs/group/RISE/sw7/modules
    module load vasp/vasp-5.4.1a

    mpirun  vasp_std''' %abbrev_name

    write_pbs.write(pbs)
    os.chdir('../')
# -----------------------------------------------------------------------------------------------------------