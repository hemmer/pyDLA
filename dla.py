#!/usr/bin/env python

import numpy as np

# constants
twopi = 2 * np.pi

# lattice goes from -L : L 
L = 10
latticesize = (2 * L + 1, 2 * L + 1)

lattice = np.zeros(latticesize, dtype=np.int8)
lattice[L, L] = 1


radius = 5              # starting radius for walkers
numParticles = 1000     # how many walkers to release

for particle in range(0, numParticles):

    # find angle on [0, 2pi)
    pos = np.exp(1j * np.random.rand() * twopi)
    # and convert to a starting position
    x = round(pos.real * radius) + L
    y = round(pos.imag * radius) + L

    lattice[x, y] = 1

print lattice
