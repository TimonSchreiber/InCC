from .boolean_expr import *

class SequenceExpression(InterpretedExpression):
    def __init__(self, seq):
        self.seq = seq

    def eval(self, env):
        for e in self.seq:
            r, env = e.eval(env)
        return (r, env)
