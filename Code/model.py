# Dual-objective optimization model: defines decision variables, objective functions (cost & supply risk), and solver setup.

# I write in python -> pyomo (translates into math) -> solver

from pyomo.environ import (ConcreteModel, Set, Var, Binary, NonNegativeReals, Objective, minimize)
    # model container	m = ConcreteModel()
    # index collections	m.E, m.T, m.L, m.R
