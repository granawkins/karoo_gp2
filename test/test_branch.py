from karoo_gp import Operator, Terminal, Branch
import numpy as np

tree_type = 'f'
depth = 3

def test_branch_initialize(rng, operators, terminals):
    b = Branch.generate(rng, operators, terminals, tree_type, depth)

    assert type(b.node) == Operator
    assert b.tree_type == 'f'
    assert b.parent == None
    assert len(b.children) == 2

    assert b.__repr__() == "<Branch: <Operator: +(binary)>>"

    assert b.parse() == 'b/2/3/c+b/1/b+1'

    b2 = b.duplicate()
    assert b2.parse() == 'b/2/3/c+b/1/b+1'


def test_branch_navigate(rng, operators, terminals):
    b = Branch.generate(rng, operators, terminals, tree_type, depth)

    assert b.n_children() == 14

    node, i = b.get_child(12)
    assert node.parse() == 'b+1'
    assert i == 0

    b2 = Branch.generate(rng, operators, terminals, tree_type, 1)
    found, i = b.set_child(12, b2)
    assert found == True
    assert i == 4
    node, i = b.get_child(12)
    assert node.parse() == 'a-c'

def test_branch_mutate(rng, operators, terminals):
    b = Branch.generate(rng, operators, terminals, tree_type, depth)

    b_ch, _ = b.get_child(12)
    b_ch.mutate(rng, operators, terminals)
    assert b.parse() == 'b/2/3/c+b/1/b-1'
    #                                 ^

    b_ch, _ = b.get_child(12)
    b_ch.mutate(rng, operators, terminals, recursive=True)
    assert b.parse() == 'b/2/3/c+b/1/a+c'
    #                                ^^^