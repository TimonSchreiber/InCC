from .ite_expr import *

class LockExpression(InterpretedExpression):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def eval(self, env):
        r, env1 = self.body.eval(env)
        return (r, env1)
    # TODO ??
