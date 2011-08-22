#!/usr/bin/env python

import numpy as np
from pylab import *

# constants
twopi = 2 * np.pi

hits = 0
birthradius = 5             # starting radius for walkers
deathradius = 10            # radius to kill off walkers
maxradius = -1              # the extent of the growth
numParticles = 1000      # how many walkers to release


# returns whether site pos = (x, y) has
# an occupied nearest-neighbour site
def nnOccupied(pos):

    # convert for lattice to array coords
    xtemp = pos[0] + L
    ytemp = pos[1] + L

    # periodic BCs
    xn = (xtemp - 1), (xtemp + 1)
    yn = (ytemp - 1), (ytemp + 1)

    if lattice[xtemp, yn[0]] != 0 or lattice[xtemp, yn[1]] != 0 or \
        lattice[xn[0], ytemp] != 0  or lattice[xn[1], ytemp] != 0:
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


L = 200             # lattice goes from -L : L
size = 2 * L + 1    # so total lattice with is 2L + 1

# preallocate and initialise centre point as "seed"
lattice = np.zeros((size, size), dtype=np.int32)
lattice[L, L] = 1


for particle in range(0, numParticles):

    # find angle on [0, 2pi)
    pos = np.exp(1j * np.random.rand() * twopi)
    # and convert to a starting position
    x = int(pos.real * birthradius)
    y = int(pos.imag * birthradius)
    pos = [x, y]

    isDead = False      # walker starts off alive

    while not isDead:

        # pick a gaussian distributed step-length
        # on [-inf,+inf] and round, ignoring zero
        # length steps
        stepLength = int(round(np.random.randn()))
        if stepLength == 0:
            continue
        stepInc = cmp(stepLength, 0)

        # decide whether to move
        # horizontally - 0
        # vertically - 1
        moveDir = np.random.randint(2)

        for step in range(0, abs(stepLength)):

            #print "step:", step, pos, nnOccupied(pos), inCircle(pos), \
                #"dir",moveDir,"sl",stepLength, stepInc,
            # stop if neighouring site is occupied
            if nnOccupied(pos):
                registerHit(pos)
                isDead = True
                break
            elif not inCircle(pos):
                isDead = True
                break
            else:
                # move the walker
                pos[moveDir] += stepInc
        #print "pos:",pos

# select only the interesting parts
#M = maxradius
#grph = L - M, L + M

#xaxis = arange(-M, M + 1)
#yaxis = arange(-M, M + 1)
#pcolormesh(xaxis, yaxis, lattice[grph[0]:grph[1], grph[0]:grph[1]])
#show()
