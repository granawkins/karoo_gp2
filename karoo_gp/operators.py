import numpy as np

operator_dict = {'+': dict(op_type='arithmetic', arity=2),
                 '-': dict(op_type='arithmetic', arity=2),
                 '*': dict(op_type='arithmetic', arity=2),
                 '/': dict(op_type='arithmetic', arity=2),
                 '**': dict(op_type='arithmetic', arity=2),
                 'neg': dict(op_type='logic', arity=1),
                 'and': dict(op_type='logic', arity=2),
                 'or': dict(op_type='logic', arity=2),
                 'not': dict(op_type='logic', arity=1),
                 '==': dict(op_type='logic', arity=2),
                 '!=': dict(op_type='logic', arity=2),
                 '<': dict(op_type='logic', arity=2),
                 '<=': dict(op_type='logic', arity=2),
                 '>': dict(op_type='logic', arity=2),
                 '>=': dict(op_type='logic', arity=2),
                 'abs': dict(op_type='math', arity=1),
                 'sign': dict(op_type='math', arity=1),
                 'square': dict(op_type='math', arity=1),
                 'sqrt': dict(op_type='math', arity=1),
                 'pow': dict(op_type='math', arity=1),
                 'log': dict(op_type='math', arity=1),
                 'log1p': dict(op_type='math', arity=1),
                 'cos': dict(op_type='math', arity=1),
                 'sin': dict(op_type='math', arity=1),
                 'tan': dict(op_type='math', arity=1),
                 'acos': dict(op_type='math', arity=1),
                 'asin': dict(op_type='math', arity=1),
                 'atan': dict(op_type='math', arity=1)}

class Operator:
    """A branch node containing an operator"""
    def __init__(self, symbol):
        if symbol not in operator_dict:
            raise ValueError("Unrecognized operator key:", symbol)
        self.symbol = symbol
        self.op_type = operator_dict[symbol]['op_type']
        self.arity = operator_dict[symbol]['arity']

    def __repr__(self):
        return f"<Operator: {self.symbol}({self.op_type})>"

class Operators():
    def __init__(self, ops):
        self.operators = [Operator(o) for o in ops]

    def __repr__(self):
        o_string = "".join([o.symbol for o in self.operators])
        return f"<Operators: {len(self.operators)}({o_string[:10]})>"

    def get(self):
        return self.operators

    @classmethod
    def load(cls, op_types):
        ops = []
        for k, v in operator_dict.items():
            if v['op_type'] in op_types:
                ops.append(k)
        return cls(ops)

    @classmethod
    def arithmetic(cls): return cls.load(['arithmetic'])
    @classmethod
    def logic(cls): return cls.load(['logic'])
    @classmethod
    def math(cls): return cls.load(['math'])

