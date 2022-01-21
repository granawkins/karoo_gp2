class Solver:
    def __init__(self, solver_type):
        self.s_type = solver_type
        self.cache = {}

    def __repr__(self):
        return f"<Solver: {self.s_type}>"

##################
#     NUMPY      #
##################
import operator as op
import numpy as np
import ast

class NumpySolver(Solver):
    def __init__(self):
        super().__init__(solver_type='Numpy')
        self.operators = {ast.Add: op.add, # e.g., a + b
                          ast.Sub: op.sub, # e.g., a - b
                          ast.Mult: op.mul, # e.g., a * b
                          ast.Div: op.truediv, # e.g., a / b
                          ast.Pow: op.pow, # e.g., a ** 2
                          ast.USub: op.neg} # e.g., -a

    def evaluate(self, population, train_data, train_labels):
        train_data = np.array(train_data)
        variables = list(population.terminals.variables.keys())
        terminals = {t: train_data[:, i] for i, t in enumerate(variables)}
        for tree in population.trees:
            expr = str(tree.sym())
            if expr in self.cache:
                fitness = self.cache[expr]
            else:
                result = self.parse_expr(expr, terminals)
                fitness_func = lambda a, b: np.sum(op.abs(a - b))
                fitness = fitness_func(result, train_labels)
                self.cache[expr] = fitness
            tree.fitness = fitness

    def parse_expr(self, expr, terminals):
        tree = ast.parse(expr, mode='eval').body
        return self.parse_node(tree, terminals)

    def parse_node(self, node, terminals):
        if isinstance(node, ast.Name):
            return terminals[node.id]

        elif isinstance(node, ast.Num):
            shape = len(terminals[list(terminals.keys())[0]])
            return np.full(shape, node.n, dtype=np.float32)

        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](
                self.parse_node(node.operand, terminals))

        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](
                self.parse_node(node.left, terminals),
                self.parse_node(node.right, terminals))


##################
#   TENSORFLOW   #
##################

# Tensorflow takes ~10s to load, so only load the module if/when its used.
from karoo_gp.util import LazyLoader
tf = LazyLoader('tf', globals(), 'tensorflow.compat.v1')

class TensorflowSolver(Solver):
    def __init__(self):
        super().__init__(solver_type='Tensorflow')
        tf.disable_v2_behavior()
        self.tf_operators = {ast.Add: tf.add, # e.g., a + b
                             ast.Sub: tf.subtract, # e.g., a - b
                             ast.Mult: tf.multiply, # e.g., a * b
                             ast.Div: tf.divide, # e.g., a / b
                             ast.Pow: tf.pow, # e.g., a ** 2
                             ast.USub: tf.negative} # e.g., -a

    def parse_expr(self, expr, tensors):
        tree = ast.parse(expr, mode='eval').body
        return self.parse_node(tree, tensors)

    def parse_node(self, node, tensors):
        if isinstance(node, ast.Name):
            return tensors[node.id]

        elif isinstance(node, ast.Num):
            shape = tensors[list(tensors.keys())[0]].get_shape()
            return tf.constant(node.n, shape=shape, dtype=tf.float32)

        elif isinstance(node, ast.UnaryOp):
            return self.tf_operators[type(node.op)](self.parse_node(node.operand, tensors))

        elif isinstance(node, ast.BinOp):
            return self.tf_operators[type(node.op)](self.parse_node(node.left, tensors), self.parse_node(node.right, tensors))



    def evaluate(self, population, train_data, train_labels):

        # Setup Tensorflow
        tf_device = "/gpu:0"
        tf_device_log = False
        config = tf.ConfigProto(
            log_device_placement=tf_device_log,
            allow_soft_placement=True)
        config.gpu_options.allow_growth = True

        # Iterate thru trees
        for i, tree in enumerate(population.trees):
            expr = str(tree.sym())
            if expr in self.cache:
                tree.fitness = self.cache[expr]
                continue
            tf.reset_default_graph()
            with tf.Session(config=config) as sess:
                with sess.graph.device(tf_device):

                    # Load solutions onto graph
                    solution = tf.constant(train_labels, dtype=tf.float32)

                    # Load constants (sample data) onto graph
                    tensors = {}
                    train_data = np.array(train_data)
                    for i, t in enumerate(population.terminals.variables.values()):
                        tensors[t.symbol] = tf.constant(train_data[:, i], dtype=tf.float32)

                    # Load tree onto graph
                    result = self.parse_expr(expr, tensors)

                    # Load fitness function onto graph
                    pairwise_fitness = tf.abs(solution - result)
                    fitness = tf.reduce_sum(pairwise_fitness)

                    # Execute graph and save results
                    result, solution, fitness, pairwise_fitness = sess.run(
                        [result, solution, fitness, pairwise_fitness])
                    tree.fitness = fitness
                    self.cache[expr] = fitness
