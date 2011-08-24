#!/usr/bin/env python

import time
from math import pi, sqrt, cos, sin
from random import choice, random, seed

from pylab import pcolormesh, axes, show
from numpy import zeros, int32, arange


class dla(object):

    def __init__(self, numParticles, L=500):
        self.L = L              # lattice goes from -L : L
        size = (2 * L) + 1      # so total lattice width is 2L + 1
        self.numParticles = numParticles    # how many walkers to release

        self.hits = 0                       # how many seeds have stuck
        self.birthradius = 5                # starting radius for walkers
        self.deathradius = 10               # radius to kill off walkers
        self.maxradius = -1                 # the extent of the growth
        seed(42)                    # seed for debugging

        # preallocate and initialise centre point as "seed"
        self.lattice = zeros((size, size), dtype=int32)
        self.lattice[L, L] = -1

        # possible (relative) nearest neighbour sites
        self.nnsteps = ((0, 1), (0, -1), (1, 0), (-1, 0))
        # possible (absolute) nearest neighbour sites
        self.nnstepsLattice = ((L, L + 1), (L, L - 1), (L + 1, L), (L - 1, L))

    # returns whether site pos = (x, y) has
    # an occupied nearest-neighbour site
    def nnOccupied(self, pos):

        # convert from lattice coords to array coords
        for step in self.nnstepsLattice:
            if self.lattice[pos[0] + step[0], pos[1] + step[1]]:
                return True
        else:
            return False
    # end of nnOccupied

    # check if a point is within the
    # allowed radius
    def inCircle(self, pos):
        # faster than sqrt
        if (pos[0] ** 2 + pos[1] ** 2) > self.deathradius ** 2:
            return False
        else:
            return True
    # end of inCircle

    # registers an extension on the seed
    def registerHit(self, pos):

        # check if this "hit" extends the max radius
        norm2 = (pos[0] ** 2 + pos[1] ** 2)
        if norm2 > self.maxradius ** 2:
            self.maxradius = int(sqrt(norm2))

            self.birthradius = self.maxradius + 5 \
                if (self.maxradius + 5) < self.L else self.L
            self.deathradius = self.maxradius + 20 \
                if (self.maxradius + 20) < self.L else self.L

        self.hits += 1
        self.lattice[pos[0] + self.L, pos[1] + self.L] = self.hits
    # end of registerHit

    # main logic loop
    def main(self):

        starttime = time.time()
        print "Running", self.numParticles, "particles..."

        # 2*pi for choosing starting position
        twopi = 2 * pi
        for particle in xrange(self.numParticles):

            # find angle on [0, 2pi)
            angle = random() * twopi
            # and convert to a starting position, pos = (x, y),
            # on a circle of radius "birthradius" around the centre seed
            pos = [int(sin(angle) * self.birthradius), \
                int(cos(angle) * self.birthradius)]

            while True:

                # pick one of the nearest neighbour sites to explore
                moveDir = choice(self.nnsteps)
                # and apply the selected move to position coordinate, pos
                pos[0] += moveDir[0]
                pos[1] += moveDir[1]

                if not self.inCircle(pos):
                    break
                elif self.nnOccupied(pos):
                    self.registerHit(pos)
                    break
        endtime = time.time()
        print "Ran in time:", (endtime - starttime)
        print "Maximum radius:", self.maxradius

    # use matplotlib to plot a heat map
    # hotter colours mean newer parts of the fractal
    def plotLattice(self):

        # select only the interesting parts
        M = self.maxradius
        grph = self.L - M, self.L + M

        # and plot
        axis = arange(-M, M + 1)
        pcolormesh(axis, axis, self.lattice[grph[0]:grph[1], grph[0]:grph[1]])
        axes().set_aspect('equal', 'datalim')
        show()

# run the main program
model = dla(5000)
model.main()
model.plotLattice()
