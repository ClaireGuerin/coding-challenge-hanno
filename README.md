# coding-challenge-hanno
Coding challenge assigned by Hanno Hildenbrandt for a programmer position at RUG

Branch|Travis|CodeCov
---|---|---
master|[![Build Status](https://www.travis-ci.com/ClaireGuerin/coding-challenge-hanno.svg?branch=main)](https://www.travis-ci.com/ClaireGuerin/coding-challenge-hanno)|[![codecov](https://codecov.io/gh/ClaireGuerin/coding-challenge-hanno/branch/main/graph/badge.svg?token=IXKD9GDK7P)](https://codecov.io/gh/ClaireGuerin/coding-challenge-hanno)
develop|[![Build Status](https://www.travis-ci.com/ClaireGuerin/coding-challenge-hanno.svg?branch=develop)](https://www.travis-ci.com/ClaireGuerin/coding-challenge-hanno)|[![codecov](https://codecov.io/gh/ClaireGuerin/coding-challenge-hanno/branch/develop/graph/badge.svg?token=IXKD9GDK7P)](https://codecov.io/gh/ClaireGuerin/coding-challenge-hanno)

## Model description

In this model, a population of preys roams around and collects resources from a bounded ecosystem. The ecosystem is a squared grid of a defined size. Predation risk is constant and diffused over the whole grid. Over a specific amount of time steps, an individual will repeat a routine as follows:

1. move on the ecosystem grid by one step, that is to say to a neighbouring grid cell. The destination cell is chosen randomly from the neighbouring cells (including the origin cell: the individual can stay on the same cell over one time step).
2. gather resources within their current cell, and add them to their storage. Let us consider there is a total of R resources in the cell at the time. When there are several individuals in the cell, they share the resources fairly as follows:

<img src="https://latex.codecogs.com/svg.latex?R\alpha\frac{\sum_{i=1}^n(1-v_i)}{n\gamma}" title="R\alpha\frac{\sum_{i=1}^n(1-v_i)}{n\gamma}" />

Where alpha is the gathering efficiency, n is the number of individuals in the cell, gamma is the competition level and v is the individual's vigilance level against predation. Vigilance is an evolving trait subject to mutation and natural selection, and is continuous (from 0 to 1). Kin selection being virtually inexistant in this model, and the sharing of resources representing a form of public good game, one could expect vigilance to tend to zero over time. However, vigilance is also under positive selection as it increases an individual's chances of survival.
3. the individual dies due to predation or survives to the next time step. The predation risk p is constant, and is defined by the probability for a prey to be eaten by a predator, in absence of vigilance. An individual's vigilance mitigates this risk, so that the probability to die at this time step is:

<img src="https://latex.codecogs.com/svg.latex?p(1-v_i)" title="p(1-v_i)" />

Resources in a cell grow at each time step at a growth rate r. If the cell was empty and hence not raided for resources by the preys, the amount of resources in the cell at the next time step is R x r. Otherwise, it is:

<img src="https://latex.codecogs.com/svg.latex?R(1-\alpha\frac{\sum_{i=1}^n(1-v_i)}{n\gamma})r" title="R(1-\alpha\frac{\sum_{i=1}^n(1-v_i)}{n\gamma})r" />

After a number of time steps (user-defined), the individuals who survived reproduce according the resources they managed to store. The more resources in their storage, the higher their fertility. The number of offpsring produced by an individual follows a Poisson distribution where fertility is the mean. The next generation is produced following a Moran process: all offspring go into a pool, from which a fixed number of individuals is randomly selected to form the new generation. Offspring inherit their parents' vigilance level (subject to mutation), and start off on the grid cell where their parents were during reproduction. Generations are non-overlapping: all parents die after reproduction. As a result, the population size at the beginning of each life cycle is always the same. It may decrease over time until reproduction, due to predation. In the event where all individuals of a generation were to die from predation, the population goes extinct and the simulation stops.

