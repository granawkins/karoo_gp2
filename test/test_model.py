from karoo_gp import Model, Population, NumpySolver, Terminals
import numpy as np
from pytest import approx

def test_model_initialization(operators, terminals):
    m = Model(operators, terminals)
    assert type(m.population) == Population
    assert type(m.rng) == np.random.RandomState
    assert type(m.solver) == NumpySolver
    assert str(m) == "<Model: <Population: 100 trees> Fittest: <Tree: 'b/(6*c) + 2'>>"

def test_model_training(operators, training):
    train_data, train_labels = training
    m = Model(operators, Terminals(['p', 'a']))

    m.train(train_data, train_labels)
    assert len(m.population.trees) == 67
    assert m.fittest().sym() == 1
