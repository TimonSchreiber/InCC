from .ite_expr import *

class LockExpression(InterpretedExpression):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def eval(self, env):
        env.lock_variable(self.var)
        r, env = self.body.eval(env)
        env.unlock_variable(self.var)
        return (r, env)
