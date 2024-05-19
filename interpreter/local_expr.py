from .lock_expr import *

class LocalExpression(InterpretedExpression):
    def __init__(self, var, value, body):
        self.var = var
        self.value = value
        self.body = body

    def eval(self, env):
       env1 = Enviroment()
       env1.set_parent(env)
       val, env1 = self.value.eval(env1)
       env1[self.var] = val
       y, _ = self.body.eval(env1)
       return y, env

