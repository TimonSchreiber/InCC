from .ite_expr import *

class LockExpression(InterpretedExpression):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def eval(self, env):
        val = self.var
        r, env = self.body.eval(env)
        env[self.var: val]
        return (r, env)
