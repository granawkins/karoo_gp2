from karoo_gp import Operator, Operators

def test_operator():
    op = Operator('+')
    assert op.symbol == '+'
    assert op.op_type == 'arithmetic'
    assert op.arity == 2
    assert op.__repr__() == '<Operator: +(arithmetic)>'

def test_operators():
    ops = Operators(['+', '-'])
    assert len(ops.get()) == 2
    assert ops.operators[0].symbol == '+'

    a_ops = Operators.arithmetic()
    assert len(a_ops.get()) == 5

    l_ops = Operators.logic()
    assert len(l_ops.get()) == 10

    m_ops = Operators.math()
    assert len(m_ops.get()) == 13
