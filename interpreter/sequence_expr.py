from .boolean_expr import *

class SequenceExpression(InterpretedExpression):
    def __init__(self, seq):
        self.seq = seq

    def eval(self, env: Enviroment):
        for expr in self.seq:
            res, env = expr.eval(env)
        return (res, env)
