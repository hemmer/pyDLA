#!/usr/bin/env python
import time

from pylab import pcolormesh, axes, show
import numpy as np

L = 2000                    # lattice goes from -L : L
SIZE = (2 * L) + 1          # so total lattice width is 2L + 1
NNSTEPS = np.array([
    (0, 1), 
    (0, -1), 
    (1, 0), 
    (-1, 0)
])
CHUNK_SIZE = 1000

class Simulation(object):
    def __init__(self, num_particles):
        self.hits = 0
        self.birthradius = 5
        self.deathradius = 10
        self.maxradius = -1

        self.lattice = np.zeros((SIZE, SIZE), dtype=np.int32)
        self.lattice[L, L] = -1
        # initialize center point as the seed

        self.hit_zone = np.zeros((SIZE, SIZE), dtype=bool)
        self.hit_zone[L, L] = True
        self.hit_zone[ NNSTEPS[:,0] + L, NNSTEPS[:,1] + L ] = True
        # the hit_zone is all of the position next to places that have
        # actually hit, these count as hits

        self.num_particles = num_particles

    def register_hit(self, pos):
        neighbors = NNSTEPS + pos
        self.hit_zone[neighbors[:,0], neighbors[:,1]] = True
        # update hit_zone

        # check if this "hit" extends the max radius
        norm2 = (pos[0] - L)**2 + (pos[1] - L)**2
        if norm2 > self.maxradius ** 2:
            self.maxradius = int(np.sqrt(norm2))
            self.birthradius = min(self.maxradius + 5, L)
            self.deathradius = min(self.maxradius + 20, L)

        self.hits += 1
        self.lattice[pos] = self.hits


    def run(self):

        # predetermine starting angles for all 
        # particles on [0, 2pi)
        angles = np.random.rand(self.num_particles) * 2 * np.pi

        for particle in xrange(self.num_particles):
            # and convert to a starting position, pos = (x, y),
            # on a circle of radius "birthradius" around the centre seed
            pos = (np.sin(angles[particle]) * self.birthradius + L,\
                    np.cos(angles[particle]) * self.birthradius + L)

            while True:
                # generate CHUNK_SIZE different moves from [0,3]
                moves = np.random.randint(0, 4, CHUNK_SIZE)
                # perform a cumulative sum so that each subsequent 
                # array position is the netx step
                moves = np.cumsum(NNSTEPS[moves], axis = 0)

                # add starting position to all of that
                moves[:,0] += pos[0]
                moves[:,1] += pos[1]

                # calculate distance to center for all the points
                from_center = moves - L
                distances_to_center = from_center[:,0]**2 + from_center[:,1]**2
                alive = distances_to_center < self.deathradius ** 2
                alive = np.minimum.accumulate(alive)

                particle_hits = self.hit_zone[moves[:,0], moves[:,1]]

                if np.any(particle_hits):
                    first_hit = particle_hits.nonzero()[0][0]
                    if alive[first_hit]:
                        pos = tuple(moves[first_hit])
                        self.register_hit(pos)
                        break
                else:
                    if np.all(alive):
                        pos = tuple(moves[-1])
                    else:
                        break

NUMBER_PARTICLES = 10000
def main():

    #np.random.seed(42)
    simulation = Simulation(NUMBER_PARTICLES)
    starttime = time.time()
    print "Running", NUMBER_PARTICLES, "particles..."
    simulation.run()
    endtime = time.time()
    print "Ran in time:", (endtime - starttime)
    print "Maximum radius:", simulation.maxradius

    ## select only the interesting parts
    #M = simulation.maxradius
    #grph = L - M, L + M

    ## and plot
    #axis = np.arange(-M, M + 1)
    #pcolormesh(axis, axis, simulation.lattice[grph[0]:grph[1], grph[0]:grph[1]])
    #axes().set_aspect('equal', 'datalim')
    #show()

if __name__ == '__main__':
    main()
