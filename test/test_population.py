import numpy as np
from karoo_gp import Population

def test_population(rng, operators, terminals):
    p = Population.generate(rng, operators, terminals)
    assert len(p.trees) == 100
    assert p.__repr__() == '<Population: 100 trees>'
