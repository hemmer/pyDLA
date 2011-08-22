#!/usr/bin/env python

import numpy as np

# constants
twopi = 2 * np.pi


# returns whether site (x, y) has
# an occupied nearest-neighbour site
def nnOccupied(x, y):
    xn = (x - 1) % size, (x + 1) % size
    yn = (y - 1) % size, (y + 1) % size

    #print x, y
    #print xn, yn

    if lattice[x, yn[0]] != 0 or lattice[x, yn[1]] != 0 or \
        lattice[xn[0], y] != 0  or lattice[xn[1], y] != 0 :

        return True
    else:
        return False
# end of nnOccupied



# lattice goes from -L : L 
L = 10
size = 2 * L + 1

lattice = np.zeros((size, size), dtype=np.int8)
lattice[L, L] = 1

print nnOccupied( 0, L-1)

radius = 5              # starting radius for walkers
numParticles = 100      # how many walkers to release

for particle in range(0, numParticles):

    # find angle on [0, 2pi)
    pos = np.exp(1j * np.random.rand() * twopi)
    # and convert to a starting position
    x = round(pos.real * radius) + L
    y = round(pos.imag * radius) + L

    #lattice[x, y] = 1

    # decide whether to move
    # vertically - 0
    # horizontally - 1
    moveDir = np.random.randint(2)
    stepLength = np.random.randn()
    #print moveDir, stepLength

print lattice
