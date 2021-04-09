# coding-challenge-hanno
Coding challenge assigned by Hanno Hildenbrandt for a programmer position at RUG

Branch|Travis|CodeCov
---|---|---
master|[![Build Status](https://www.travis-ci.com/ClaireGuerin/coding-challenge-hanno.svg?branch=main)](https://www.travis-ci.com/ClaireGuerin/coding-challenge-hanno)|[![codecov](https://codecov.io/gh/ClaireGuerin/coding-challenge-hanno/branch/main/graph/badge.svg?token=IXKD9GDK7P)](https://codecov.io/gh/ClaireGuerin/coding-challenge-hanno)
develop|[![Build Status](https://www.travis-ci.com/ClaireGuerin/coding-challenge-hanno.svg?branch=develop)](https://www.travis-ci.com/ClaireGuerin/coding-challenge-hanno)|[![codecov](https://codecov.io/gh/ClaireGuerin/coding-challenge-hanno/branch/develop/graph/badge.svg?token=IXKD9GDK7P)](https://codecov.io/gh/ClaireGuerin/coding-challenge-hanno)

## Model description

In this model, a population of preys roams around and collects resources from a bounded ecosystem. The ecosystem is a squared grid of a defined size. Predation risk is constant and diffused over the whole grid. Over a specific amount of time steps, an individual will repeat a routine as follows:

1. move on the ecosystem grid by one step, that is to say to a neighbouring grid cell. The destination cell is chosen randomly from the neighbouring cells (including the origin cell: the individual can stay on the same cell over one time step).
2. gather resources within their current cell. Considering there is a total of $R$ resources in the cell at the time. When there are several individuals in the cell, they share the resources fairly as follows:
$\R\alpha\frac{\sum_{i=1}^n(1-v_i)}{n\gamma}$

