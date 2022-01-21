from pytest import approx
from karoo_gp import Solver, NumpySolver, TensorflowSolver, Population, Terminals

def test_solver():
    s = Solver('anon')
    assert type(s) == Solver
    assert str(s) == "<Solver: anon>"

def solver_test_func(solver, rng, operators, training):
    terminals = Terminals(['p', 'a'])
    population = Population.generate(rng, operators, terminals)
    train_data, train_labels = training
    solver.evaluate(population, train_data, train_labels)
    assert len(solver.cache) == 87
    assert len(population.trees) == 100
    for t in population.trees:
        assert t.fitness is not None
    assert str(population.trees[0].sym()) == '2*a + a/p**3 + 1'
    assert population.trees[0].fitness == approx(246.29974)

def test_numpy_solver(rng, operators, training):
    solver = NumpySolver()
    assert str(solver) == "<Solver: Numpy>"
    solver_test_func(solver, rng, operators, training)

# SLOOOOOWWW
# def test_tensorflow_solver(rng, operators, training):
#     solver = TensorflowSolver()
#     assert str(solver) == "<Solver: Tensorflow>"
#     solver_test_func(solver, rng, operators, training)
