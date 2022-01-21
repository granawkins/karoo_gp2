from karoo_gp import Tree

DEFAULT_POPULATION = dict(tree_type='r',
                          population_size=100)

class Population:
    def __init__(self, rng, operators, terminals, params={}):
        self.operators = operators
        self.terminals = terminals
        self.trees = []
        # TODO: Add history: [max fitness of prev generations]
        # TODO: Add signature: hash(variables + operators)

        # Generate initial population
        population_size = params.pop('population_size', DEFAULT_POPULATION['population_size'])
        tree_type = params.get('tree_type', DEFAULT_POPULATION['tree_type'])
        args = (rng, operators, terminals)
        if tree_type == 'r':
            for i in range(population_size):
                if i % 2 == 0:
                    self.trees.append(Tree.generate(*args, {**params, 'tree_type': 'f'}))
                else:
                    self.trees.append(Tree.generate(*args, {**params, 'tree_type': 'g'}))
        elif tree_type in ['f', 'g']:
            self.trees = [Tree.generate(*args, params) for _ in range(population_size)]
        else:
            raise ValueError("Unrecognized tree_type:", tree_type)

    def __repr__(self):
        return f"<Population: {len(self.trees)} trees>"
