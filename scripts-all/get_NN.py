'''
JTSivak 06.04.2022

What it does
------------
Gets the nearest neighbors for user specified elements and cutoff distance within a given structure.
------------

User input/changes
------------
1. change name of inputted file for the variable 's'
2. define the cutoff dictionary of the different elements are taken into account as well as the distance (in Angstroms) to search over
3. the atom index in the structure that you wish to get specific neighbor distances for
    - NOTE that you need to have these be the exact same as the structural file that is inputted
------------

Outputs
------------
prints out -->
    structure inputted 
    element-element interactions chosen
    cutoff distance considered
    each atom index with the specified neighbor distances
------------
'''


from pymatgen.core.structure import Structure
from pymatgen.analysis.local_env import CutOffDictNN

# NEED USER CHANGES
# -----------------------------------------------
s = Structure.from_file("./POSCAR_J14_vacancy_6.25%_higherspin") # just change the filename

cutoff_dict = {('Ni', 'H'):7} # specify the element-element interaction and cutoff distance (in Angstroms) to be used
    # NOTE the output does not include the element with the distances, so it is easier to just use two elemental species here

N = [236, 237, 238, 239] # these are the atom index numbers within the inputted structure above that you wish to analyze their NNs
    # NOTE that these will be the only atoms considered for the element-element interactions specified in cutoff_dict above
    # NOTE that these sometimes start at index # 0, so check in the printed structural information from the output
# -----------------------------------------------

print(s)

NN = CutOffDictNN(cut_off_dict=cutoff_dict)
print("\n\ncutoff dictionary used:\n" + str(cutoff_dict) +"\n")

for i in range(len(N)):
    print("\natom index = {}\n---------------".format(N[i]))
    info = NN.get_nn_info(s, N[i])

    for j in range(len(info)):
        print("{:.3f}\tAngstroms".format(info[j]['weight']))
