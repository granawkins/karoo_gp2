from karoo_gp import Tree, Branch
import numpy as np

expected_display = '''
                     ________+____________________
           ________/__________                ___-_____
      ___*_____           ___+_____         a         b
    3         3         1         b
'''

def test_tree_initialize(capsys, rng, operators, terminals):
    t = Tree.generate(rng, operators, terminals)

    assert t.fitness == None
    assert type(t.root) == Branch
    assert t.root.n_children() == 10
    assert str(t.sym()) == 'a + 9'
    assert t.__repr__() == "<Tree: 'a + 9'>"

    t2 = Tree.generate(rng, operators, terminals, {'depth': 4, 'tree_type': 'f'})
    assert t2.root.n_children() == 30
    assert str(t2.sym()) == '-4*a/3 - b + c - 10 - c/a'

    # TODO: Fix
    # disp = t.display()
    # print(disp)
    # assert capsys.readouterr().out == expected_display


def test_tree_mutate(rng, operators, terminals):
    t = Tree.generate(rng, operators, terminals, {'depth': 5})
    assert str(t.parse()) == '3+3*b-a+b/b/1+2/1-2*1-1-1+3-2'

    t.point_mutate(rng, operators, terminals)
    assert str(t.parse()) == '3+1*b-a+b/b/1+2/1-2*1-1-1+3-2'
    #                           ^

    t.full_mutate(rng, operators, terminals)
    assert str(t.parse()) == '3+1*b-a+b/b/1+2/2-2*1-1-1+3-2'
    #                                         ^
    t.full_mutate(rng, operators, terminals)
    assert str(t.parse()) == '3+1*b-a+b/b/1+a+a-1*2+2/b*c-c'
    #                                     ^^^^^^^^^^^^^^^^^

    t2 = Tree.generate(rng, operators, terminals, {'depth': 4})
    assert str(t2.parse()) == '3+c-b/c+c*1*2+3+a*c-2'
    assert t2.root.node.symbol == '+'
    t3 = t.crossover(rng, t2)
    assert str(t3.parse()) == '3+1*b-a+b/b/1+a+a-1*2+2/c*1*2+3+a*c-2*c-c'
    #                                                  ^^^^^^^^^^^^^
