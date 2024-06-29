from .ite_expr import *

class LockExpression(InterpretedExpression):
    def __init__(self, vars, body):
        self.vars = vars
        self.body = body

    def eval(self, env: Enviroment):
        env.lock_variables(self.vars)
        res, env = self.body.eval(env)
        env.unlock_variables(self.vars)
        return (res, env)
