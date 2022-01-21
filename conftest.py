import pytest
import numpy as np
from karoo_gp import Operators, Terminals

@pytest.fixture()
def rng():
    return np.random.RandomState(12345)

@pytest.fixture()
def operators():
    return Operators(['*', '/', '+', '-'])

@pytest.fixture()
def terminals():
    return Terminals(['a', 'b', 'c'], constants=[1, 2, 3])
