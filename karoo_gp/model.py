import numpy as np
import operator
from karoo_gp import Population, NumpySolver, TensorflowSolver

solvers = {'numpy': NumpySolver, 'tensorflow': TensorflowSolver}

class Model:

    def __init__(self, operators, terminals, population_params={}, solver='numpy', seed=12345):
        self.rng = np.random.RandomState(seed)
        self.population = Population.generate(self.rng, operators, terminals, population_params)
        if solver not in solvers:
            raise ValueError("Unrecognized solver:", solver)
        self.solver = solvers[solver.lower()]()

    def __repr__(self):
        return f"<Model: {self.population} Fittest: {self.fittest()}>"

    def train(self, train_data, train_labels, generations=1, tournament_size=7, min_nodes=5,
              max_depth=10, evolution_params={}):

        # Build default layers
        layers = [('fitness', (self.solver, train_data, train_labels))]
        for i in range(generations):
            layers.append(('evolve', (self.rng, tournament_size, evolution_params)))
            layers.append(('cull', (min_nodes, max_depth)))
            layers.append(('fitness', (self.solver, train_data, train_labels)))

        # Process layers
        self.process(layers)

    def process(self, layers):
        for (f, args) in layers:
            func = getattr(self.population, f)
            if not func:
                raise ValueError("Unrecognized layer passed to processor:", f)
            func(*args)

    def fittest(self):
        return self.population.trees[0]
