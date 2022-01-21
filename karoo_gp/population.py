from karoo_gp import Tree
import operator
import numpy as np

DEFAULT_POPULATION = dict(tree_type='r',
                          population_size=100,
                          criteria='fitness')

DEFAULT_EVOLUTION = {'duplicate': 0.1,
                     'point_mutate': 0.1,
                     'branch_mutate': 0.2,
                     'crossover': 0.6}

class Population:
    def __init__(self, operators, terminals, population_size, criteria, trees):
        self.operators = operators  # Operators, index of all in use
        self.terminals = terminals  # Terminals, index of all in use
        self.population_size = population_size  # int
        self.criteria = criteria   # str, tree attribute to sort by
        self.trees = trees  # list, Trees
        # TODO: Add history
        # TODO: Add signature: hash(variables + operators)

    @classmethod
    def generate(cls, rng, operators, terminals, params={}):
        population_size = params.pop('population_size', DEFAULT_POPULATION['population_size'])
        criteria = params.pop('critera', DEFAULT_POPULATION['criteria'])
        tree_type = params.get('tree_type', DEFAULT_POPULATION['tree_type'])
        args = (rng, operators, terminals)
        if tree_type == 'r':
            trees = []
            for i in range(population_size):
                if i % 2 == 0:
                    trees.append(Tree.generate(*args, {**params, 'tree_type': 'f', 'switch_to_grow': True}))
                else:
                    trees.append(Tree.generate(*args, {**params, 'tree_type': 'g'}))
        elif tree_type in ['f', 'g']:
            trees = [Tree.generate(*args, params) for _ in range(population_size)]
        else:
            raise ValueError("Unrecognized tree_type:", tree_type)
        return cls(operators, terminals, population_size, criteria, trees)

    def duplicate(self):
        trees = [t.duplicate() for t in self.trees]
        return Population(self.operators, self.terminals, self.population_size,
                          self.criteria, trees)

    def __repr__(self):
        return f"<Population: {len(self.trees)} trees>"

    ###############
    #    EVOLVE   #
    ###############

    def fitness(self, solver, train_data, train_labels):
        # TODO: Build fitness function
        solver.evaluate(self, train_data, train_labels)
        self.trees.sort(key=operator.attrgetter(self.criteria))

    def tournament(self, rng, tournament_size):
        players = rng.choice(self.trees, tournament_size)
        criteria = self.criteria
        winner = min(players, key=operator.attrgetter(criteria))
        return winner

    def evolve(self, rng, tournament_size=7, evolution_params={}):
        evolved = []
        for evolve_by, ratio in DEFAULT_EVOLUTION.items():
            if evolve_by in evolution_params:
                ratio = evolution_params[evolve_by]
            n_samples = round(self.population_size * ratio)
            ops = self.operators
            ts = self.terminals
            for _ in range(n_samples):
                winner = self.tournament(rng, tournament_size)
                if evolve_by == 'duplicate':
                    offspring = winner.duplicate()
                elif evolve_by == 'point_mutate':
                    offspring = winner.duplicate()
                    offspring.point_mutate(rng, ops, ts)
                elif evolve_by == 'branch_mutate':
                    offspring = winner.duplicate()
                    offspring.full_mutate(rng, ops, ts)
                elif evolve_by == 'crossover':
                    mate = self.tournament(rng, tournament_size)
                    offspring = winner.crossover(rng, mate)
                evolved.append(offspring)
        self.trees = evolved

    def cull(self, min_nodes, max_depth):
        culled = []
        for tree in self.trees:
            if len(tree.parse()) < min_nodes or tree.depth() > max_depth:
                continue
            culled.append(tree)
        self.trees = culled
