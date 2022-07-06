# HowTo-VASP
This is a collection of my experience with VASP for performing DFT calculations on transition metal oxide systems primarily. I also use this as a memory bank of how to keep track of how to do different things and analyses. I hope that this also can help someone who is just learning how to run electronic structure calculations using hte VASP software package, but note that I am by no means an expert so be sure to do your own research. I primarily work with high-entropy oxide systems involving the highly correlated transition metal oxides (TMOs), thus a large majority of this work is focused on these systems as well as some tips and tricks which I have learned along the way. Much more comprehensive descriptions and explanations are given within the VASP Wiki (https://www.vasp.at/wiki/index.php/The_VASP_Manual). I will reference this a bunch of times througout this because it is very helpful.

***

## VASP Input Files
For VASP calculations, you need four VASP specific files as well as a submission script to the queue. More comprehensive descriptions can be found at the included links to the VASPWiki. I have provided a Python script using PyMatGen (https://pymatgen.org/) that is extremely useful when making these files and to minimize any mistakes made when generating these files.
#### INCAR
https://www.vasp.at/wiki/index.php/INCAR
This is the central input for VASP. This file describes *what we want to do* as well as *how we want to do it*, thus one needs to be very careful when setting this up. There are defaults for nearly all tags, but I would explicitly set these for consistency between calculations.

#### POSCAR
https://www.vasp.at/wiki/index.php/POSCAR
This is the file which contains all of the atomic coordinates and lattice geometries of the structure.

#### KPOINTS
https://www.vasp.at/wiki/index.php/KPOINTS
This contains the kpoint mesh to be used to sample the Brillouin zone within the calculation. One can explicitly define these, or use an automated scheme such as Monkhorst-Pack. Additionally, you define whether you want the kpoint grid centered on the $\Gamma$-point as well.

#### POTCAR
https://www.vasp.at/wiki/index.php/POTCAR
This contains the pseudopotentials for each atomic species in the calculation. It is VERY IMPORTANT that these are in the same ordr as the species within the POSCAR file. VASP will usually not even throw an error, so this is why I would *always* recommend to use PyMatGen to generate these VASP input files.

## Some INCAR flags
Going through all of these would be insanity, but I wanted to highlight a few of these here that are most important and to be careful about in my experience.
- **ENCUT**
    - This is the plane-wave cutoff – be sure to perform convergence testing w.r.t. this.
    - VERY IMPORTANT!! Make sure that if you are doing a full relaxation that you take into account Pulay Stress with having a large ENCUT. You can read more about it here: https://www.vasp.at/wiki/index.php/Energy_vs_volume_Volume_relaxations_and_Pulay_stress
    - When dealing with oxide systems, since oxygen requires a large plane-wave cutoff, you have to have ENCUT ≥ 520 eV.
- **ALGO**
    - This is the electronic minimization scheme I personally use ALGO = All (which is a conjugate gradient method) since I found some discrepancies with the default (ALGO = Normal) as well as ALGO = Fast. This is likely due to the complexity of the potential energy surface for these TMOs that I work on, especially when I have alloyed systems. *You should do testing on these for each system*, as I have found that using a more robust method, such as ALGO = All, can result in qualitative differences in results (in addition to finding lower energy states). Following the MaterialsProject order used for their high-throughput calculations, I go from least to most robust: Fast  Normal  All.
- **ISMEAR**
    - This is the smearing type for partially occupied states. I normally use Gaussian or Tetrahedral with Bloch corrections.
- **MAGMOM**
    - This controls the initial magnetic moment on a per-atom basis for spin-polarized calculations (ISPIN = 2)
    - This goes in the same ordering as the atoms in the POSCAR file.
    - An easier way to define these for each system is by using the ASE GUI. I have an example of this in /01-making-vasp-inputs/HowTo-MagneticOrderings/
- **NCORE**
    - This controls the parallelization over the compute cores that operate on an individual orbital. I have found that you can have a large amount of speed up with this tag, in addition to the KPAR tag for kpoints. I have not played around much with the KPAR tag, but supposedly this works best for calculations with a large number of kpoints so it may be useful for you.
- **IBRION**
    - This controls the ionic relaxation scheme. Conjugate gradient (IBRION = 2) is always the safest in my opinion and is what is primarily used, but it can result in ZBRENT errors where the algorithm can’t find the next step because it is too flat. In that case you should use the IBRION = 1 for a quasi-Newton type of minimization.
- **EDIFFG**
    - This controls the break condition for the ionic loop. A positive value is for energy, while a negative value is for forces. It is almost always better to use a negative value for forces, in my experience. For routine calculations, I usually use EDIFFG = -0.010, which is 10 meV/$\AA$.
- **ISYM**
    - This controls the way that VASP treat symmetry. This can play a large role in systems such as CoO rocksalt where there is a slight breaking from perfect 90o angles of the unit cell; the trade-off is that calculations can take more time since you are not using the symmetry to reduce computational cost. I usually run most calculations with ISYM = 0 to be safe.
- **NBANDS**
    - This controls the number of bands used in the calculation. For some systems with more complex magnetic orderings and/or more unpaired electrons, you will need to increase this value from the default. This is discussed on the VaspWiki here: https://www.vasp.at/wiki/index.php/Number_of_bands_NBANDS
    - One of the more common times when I have needed to increase this value is for when the system struggles to maintain the initial magnetic ordering that is given. For systems such as MnO or CoO with larger local magnetic moments, this can be seen as just one/few atoms flipping their spin state with the expected. One can also confirm that this worked by comparison of total energies from the default vs. increased NBANDS to determine if a lower energy state was found including more bands.

## To Do
- add in convergence testing examples
- add in Pulay stress example
- showing how important initial guesses are for DFT calculations going to local minima (I guess with CuO)
- examples of differences for ALGO = Fast/Normal/All for complex systems (use CoO here)
- example of need for increasing NBANDS in calculation
- start adding in scripts for analysis stuff
    - density of states
    - local environment (w.r.t vacancies and changes)