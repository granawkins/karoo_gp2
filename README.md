# karoo_gp2

This is a Genetic Programming (GP) Algorithm loosely based on [Karoo GP](https://github.com/kstaats/karoo_gp).

It currently supports regression data, and can be modified to accomodate binary and multiclass classification.

## Basic Usage
```
import pandas as pd
from karoo_gp import Terminals, Operators, Model

# Load train data
train_data = pd.read_csv('datasets/iris.csv')
train_labels = train_data.pop('s')

# Setup model
operators = Operators.arithmetic()
terminals = Terminals(train_data.keys(), constants=[.1, .2, .3, .4, .5])
model = Model(operators, terminals)

# Train model
model.train(train_data, train_labels)
model.fittest()
>>> <Tree: '0.2*pl**2/sw ...' fitness: 37.33>
```

## Get Started
```
git clone https://github.com/granawkins/karoo_gp2.git

cd karoo_gp2
```

## Demo
For a detailed guide to the different classes and model options, refer to the
Jupyter Notebook, `Demo.ipynb`.
