from karoo_gp import Operator, Operators

def test_operator():
    op = Operator('+')
    assert op.symbol == '+'
    assert op.op_type == 'binary'
    assert op.arity == 2
    assert op.__repr__() == '<Operator: +(binary)>'

def test_operators():
    ops = Operators(['+', '-'])
    assert len(ops.get()) == 2
    assert ops.operators[0].symbol == '+'
