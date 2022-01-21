import pytest
import numpy as np
import pandas as pd
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

@pytest.fixture()
def training():
    data = np.array([[0.241,0.39,0.98],
                     [.615,0.72,1.01],
                     [1.00,1.00,1.00],
                     [1.88,1.52,1.01],
                     [11.8,5.20,0.99],
                     [29.5,9.54,1.00],
                     [84.0,19.18,1.00],
                     [165,30.06,1.00],
                     [248,39.44,1.00]])
    cols = ['p', 'a', 's']
    train_data = pd.DataFrame(data=data, columns=cols)
    train_labels = train_data.pop('s')
    return train_data, train_labels
