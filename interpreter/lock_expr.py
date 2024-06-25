from .ite_expr import *

class LockExpression(InterpretedExpression):
    def __init__(self, vars, body):
        self.vars = vars
        self.body = body

    def eval(self, env):
        env.lock_variables(self.vars)
        r, env = self.body.eval(env)
        env.unlock_variables(self.vars)
        return (r, env)
