#!/usr/bin/env python

import numpy as np
from pylab import *

# constants
twopi = 2 * np.pi


# returns whether site pos = (x, y) has
# an occupied nearest-neighbour site
def nnOccupied(pos):

    # convert for lattice to array coords
    xtemp = pos[0] + L
    ytemp = pos[1] + L

    # periodic BCs
    xn = (xtemp - 1) % size, (xtemp + 1) % size
    yn = (ytemp - 1) % size, (ytemp + 1) % size

    if lattice[xtemp, yn[0]] != 0 or lattice[xtemp, yn[1]] != 0 or \
        lattice[xn[0], ytemp] != 0  or lattice[xn[1], ytemp] != 0:

        return True
    else:
        return False
# end of nnOccupied


# check if a point is within the
# allowed radius
def inCircle(pos):
    if np.sqrt(pos[0] ** 2 + pos[1] ** 2) > radius:
        return False
    else:
        return True
# end of inCircle


# converts coordinates relative
# to lattice centre
def setLattice(pos):
    lattice[pos[0] + L, pos[1] + L] = 1
# end of setLattice


L = 20              # lattice goes from -L : L
size = 2 * L + 1    # so total lattice with is 2L + 1

# preallocate and initialise centre point as "seed"
lattice = np.zeros((size, size), dtype=np.int8)
lattice[L, L] = 1

radius = 15             # starting radius for walkers
numParticles = 10000    # how many walkers to release

for particle in range(0, numParticles):


    # find angle on [0, 2pi)
    pos = np.exp(1j * np.random.rand() * twopi)
    # and convert to a starting position
    x = round(pos.real * radius)
    y = round(pos.imag * radius)

    initPos = [x, y]

    pos = [x, y]
    #print "particle:", particle, "initial pos:", pos

    #import pdb; pdb.set_trace()

    isDead = False      # walker starts off alive

    while not isDead:

        # pick a gaussian distributed step-length
        # on [-inf,+inf] and round, ignoring zero
        # length steps
        stepLength = int(round(np.random.randn()))
        if stepLength == 0: continue
        stepInc = cmp(stepLength, 0)

        # decide whether to move
        # horizontally - 0
        # vertically - 1
        moveDir = np.random.randint(2)

        #print moveDir, stepLength, stepInc

        for step in range(0, abs(stepLength)):

            #print "step:", step, pos, nnOccupied(pos), inCircle(pos), \
                #"dir",moveDir,"sl",stepLength, stepInc,
            # stop if neighouring site is occupied
            if nnOccupied(pos):
                setLattice(pos)
                isDead = True
                break
            elif not inCircle(pos):
                isDead = True
                break
            else:
                # move the walker
                pos[moveDir] += stepInc
        #print "pos:",pos

xaxis = arange(-L,L+1)
yaxis = arange(-L,L+1)
pcolormesh(xaxis, yaxis, lattice)
show()

print lattice
