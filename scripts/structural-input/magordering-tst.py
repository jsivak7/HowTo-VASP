from ase import Atoms
from ase.io import read, write
import numpy as np

s = read("NiO_POSCAR")
#print(s)

a = 4.211

tst = s.get_positions()
#print(tst)

#print("up")
spin_up = np.array([ [0, 0, 0], [0, a/2, a*1.5], [a/2, 0, a*1.5], [a/2, a/2, a], [0, a*1.5, a/2], [a/2, a, a/2], [a/2, a*1.5, 0], [0, a, a], [a, a/2, a/2], [a*1.5, 0, a/2], [a*1.5, a/2, 0.0], [a, 0, a], [a, a, 0], [a, a*1.5, a*1.5], [a*1.5, a, a*1.5], [a*1.5, a*1.5, a] ])
#print(spin_up)
up_index = []

#print("down")
spin_down = np.array([ [0, a/2, a/2], [a/2, 0, a/2], [a/2, a/2, 0], [0, 0, a], [0, a, 0], [0, a*1.5, a*1.5], [a/2, a, a*1.5], [a/2, a*1.5, a], [a, 0, 0], [a, a/2, a*1.5], [a*1.5, 0, a*1.5], [a*1.5, a/2, a], [a, a*1.5, a/2], [a*1.5, a, a/2], [a*1.5, a*1.5, 0], [a, a, a] ])
#print(spin_down)
down_index = []

for i in range(len(tst)):
    for j in range(len(spin_up)): # NOTE that this needs to be an equal amount of spin up and down currently...
        if np.array_equal(spin_up[j], tst[i]) == True:
            up_index.append(i)
        elif np.array_equal(spin_down[j], tst[i]) == True:
            down_index.append(i)

#print(up_index)
#print(down_index)

magmom = []

for i in range(len(tst)):
    if i in up_index:
        magmom.append(+2)
    elif i in down_index:
        magmom.append(-2)
    else:
        magmom.append(0)

print(magmom)