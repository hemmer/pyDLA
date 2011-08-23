#!/usr/bin/env python

from math import pi, sqrt, cos, sin
from random import choice, random, seed
import time

from pylab import pcolormesh, axes, show
from numpy import zeros, int32, arange

twopi = 2 * pi              # 2 pi for choosing starting position

hits = 0                    # how many seeds have stuck
birthradius = 5             # starting radius for walkers
deathradius = 10            # radius to kill off walkers
maxradius = -1              # the extent of the growth
numParticles = 2000         # how many walkers to release
#seed(42)                    # seed for debugging

L = 2000                    # lattice goes from -L : L
size = (2 * L) + 1          # so total lattice width is 2L + 1

# possible nearest neighbour sites
nnsteps = ((0, 1), (0, -1), (1, 0), (-1, 0))


# returns whether site pos = (x, y) has
# an occupied nearest-neighbour site
def nnOccupied(pos):

    # convert from lattice coords to array coords
    latticepos = (pos[0] + L, pos[1] + L)

    for step in nnsteps:
        if lattice[latticepos[0] + step[0], latticepos[1] + step[1]] != 0:
            return True
    else:
        return False
# end of nnOccupied


# check if a point is within the
# allowed radius
def inCircle(pos):
    if (pos[0] ** 2 + pos[1] ** 2) > deathradius ** 2:  # faster than sqrt
        return False
    else:
        return True
# end of inCircle


# registers an extension on the seed
def registerHit(pos):
    global hits, birthradius, deathradius, maxradius

    # check if this "hit" extends the max radius
    norm2 = (pos[0] ** 2 + pos[1] ** 2)
    if norm2 > maxradius ** 2:
        maxradius = int(sqrt(norm2))
        birthradius = maxradius + 5 if (maxradius + 5) < L else L
        deathradius = maxradius + 20 if (maxradius + 20) < L else L

    hits += 1
    lattice[pos[0] + L, pos[1] + L] = hits
# end of registerHit


# preallocate and initialise centre point as "seed"
lattice = zeros((size, size), dtype=int32)
lattice[L, L] = -1

starttime = time.time()

for particle in range(numParticles):

    #print particle

    # find angle on [0, 2pi)
    angle = random() * twopi
    # and convert to a starting position, pos = (x, y),
    # on a circle of radius "birthradius" around the centre seed
    pos = [int(sin(angle) * birthradius), int(cos(angle) * birthradius)]

    isDead = False      # walker starts off alive

    while not isDead:

        # pick one of the nearest neighbour sites to explore
        moveDir = choice(nnsteps)
        # and apply the selected move to position coordinate, pos
        pos[0] += moveDir[0]
        pos[1] += moveDir[1]

        if not inCircle(pos):
            isDead = True
            break
        elif nnOccupied(pos):
            registerHit(pos)
            isDead = True
            break


endtime = time.time()
print "Ran in time", (endtime - starttime)

# select only the interesting parts
M = maxradius
grph = L - M, L + M

# and plot
xaxis = arange(-M, M + 1)
yaxis = arange(-M, M + 1)
pcolormesh(xaxis, yaxis, lattice[grph[0]:grph[1], grph[0]:grph[1]])
axes().set_aspect('equal', 'datalim')
show()
