Diffusion-Limited Aggregation (Fast NumPy version by Winston Ewert)
===================================================================

Simple project to investigate [Diffusion-Limited Aggregation](http://en.wikipedia.org/wiki/Diffusion-limited_aggregation) (and teach me python). The project starts off with a single seed at the centre of a lattice. We then release [random walkers](http://en.wikipedia.org/wiki/Random_walk) at a certain radius from the seed: if they come into contact with seed they join it and a new walker is released. Conversely, if they wander too far from the centre, the walker is eliminated and a new one spawned.

To run, first download the script:

    $ git clone git://github.com/hemmer/pyDLA.git
    $ cd pyDLA

First make sure your system meets the requirements, then to run enter:

    $ ./dla.py

Updates
-------

As a result of this [forum thread](http://codereview.stackexchange.com/questions/4336/code-review-of-small-scientific-project-particuarly-array-vs-list-perform), a much faster version of the code was suggested by user Winston Ewert that uses the `NumPy` libraries more efficiently. I have uploaded this version as a branch for reference, which you can checkout using:

    $ git checkout numpyFast


Requirements
------------

This script requires the `NumPy` and `matplotlib` libraries to run. To install these on Ubuntu:

    $ sudo apt-get install python-numpy python-matplotlib
        

Examples
--------

![Crystal Growing](/hemmer/pyDLA/raw/master/img/n50000.png) . 
![Crystal Growing around a box](/hemmer/pyDLA/raw/master/img/n20000.png)
