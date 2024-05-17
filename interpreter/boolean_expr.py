from .assignment_expr import *

binary_operators |= {
    'and':  operator.and_,
    'or':   operator.or_,
    'eq':   operator.eq,
    'xor':  operator.xor,
    'neq':  operator.xor,
    'nand': lambda a,b: not (a and b),
    'nor':  lambda a,b: not (a or b),
    'impl': lambda a,b: (not a) | b
}

unary_operators |= {
    'NOT': operator.not_
}

boolean_values = {
    'TRUE':  True,
    'FALSE': False
}

class BooleanValueExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1.upper()

    def eval(self, env):
        return (boolean_values[self.e1], env)
