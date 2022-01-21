import numpy as np

operator_dict = {'+': dict(op_type='binary', arity=2),
                 '-': dict(op_type='binary', arity=2),
                 '*': dict(op_type='binary', arity=2),
                 '/': dict(op_type='binary', arity=2),
                 '**': dict(op_type='binary', arity=2),
                 'neg': dict(op_type='unary', arity=1),
                 'and': dict(op_type='bool', arity=2),
                 'or': dict(op_type='bool', arity=2),
                 'not': dict(op_type='bool', arity=1),
                 '==': dict(op_type='bool', arity=2),
                 '!=': dict(op_type='bool', arity=2),
                 '<': dict(op_type='compare', arity=2),
                 '<=': dict(op_type='compare', arity=2),
                 '>': dict(op_type='compare', arity=2),
                 '>=': dict(op_type='compare', arity=2),
                 'abs': dict(op_type='call', arity=1),
                 'sign': dict(op_type='call', arity=1),
                 'square': dict(op_type='call', arity=1),
                 'sqrt': dict(op_type='call', arity=1),
                 'pow': dict(op_type='call', arity=1),
                 'log': dict(op_type='call', arity=1),
                 'log1p': dict(op_type='call', arity=1),
                 'cos': dict(op_type='call', arity=1),
                 'sin': dict(op_type='call', arity=1),
                 'tan': dict(op_type='call', arity=1),
                 'acos': dict(op_type='call', arity=1),
                 'asin': dict(op_type='call', arity=1),
                 'atan': dict(op_type='call', arity=1)}

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

    def get(self):
        return self.operators

