#!/usr/bin/env python

import time
from random import choice, random, seed

from pylab import pcolormesh, axes, show
import numpy as np

twopi = 2 * np.pi              # 2 pi for choosing starting position

hits = 0                    # how many seeds have stuck
birthradius = 5             # starting radius for walkers
deathradius = 10            # radius to kill off walkers
maxradius = -1              # the extent of the growth
numParticles = 1000         # how many walkers to release
seed(42)                    # seed for debugging

L = 500                     # lattice goes from -L : L
size = (2 * L) + 1          # so total lattice width is 2L + 1

# preallocate and initialise centre point as "seed"
lattice = np.zeros((size, size), dtype=np.int32)
lattice[L, L] = -1

# possible (relative) nearest neighbour sites
nnsteps = np.array(((0, 1), (0, -1), (1, 0), (-1, 0)))
# account for lattice zero not being array zero
nnstepsLattice = nnsteps + L


# returns whether site pos = (x, y) has
# an occupied nearest-neighbour site
def nnOccupied(pos):

    # find neighbouring sites on lattice
    neighbours = nnstepsLattice + pos
    #print neighbours
    for nx, ny in neighbours:
        if lattice[nx, ny] != 0:
            return True
    else:
        return False
# end of nnOccupied


# check if a point is within the
# allowed radius
def inCircle(pos):
    #print "circ", pos, pos[0], deathradius
    if np.sum(pos ** 2) > deathradius ** 2:  # faster than sqrt
        return False
    else:
        return True
# end of inCircle


# registers an extension on the seed
def registerHit(pos):
    global hits, birthradius, deathradius, maxradius

    # check if this "hit" extends the max radius
    norm2 = np.sum(pos ** 2)
    if norm2 > maxradius ** 2:
        maxradius = int(np.sqrt(norm2))
        birthradius = maxradius + 5 if (maxradius + 5) < L else L
        deathradius = maxradius + 20 if (maxradius + 20) < L else L

    hits += 1
    lx, ly = pos + L
    lattice[lx, ly] = hits
# end of registerHit


starttime = time.time()
print "Running", numParticles, "particles..."

for particle in xrange(numParticles):

    #print particle

    # find angle on [0, 2pi)
    angle = random() * twopi
    # and convert to a starting position, pos = (x, y),
    # on a circle of radius "birthradius" around the centre seed
    pos = np.array((int(np.sin(angle) * birthradius), int(np.cos(angle) * birthradius)))

    isDead = False      # walker starts off alive

    while not isDead:

        # pick one of the 4 nearest neighbour sites to explore
        randMove = np.random.randint(0, 4)
        # and apply the selected move to position coordinate, pos
        pos += nnsteps[randMove]

        if not inCircle(pos):
            isDead = True
            break
        elif nnOccupied(pos):
            registerHit(pos)
            isDead = True
            break


endtime = time.time()
print "Ran in time:", (endtime - starttime)
print "Maximum radius:", maxradius

# select only the interesting parts
M = maxradius
grph = L - M, L + M

# and plot
axis = arange(-M, M + 1)
pcolormesh(axis, axis, lattice[grph[0]:grph[1], grph[0]:grph[1]])
axes().set_aspect('equal', 'datalim')
show()
