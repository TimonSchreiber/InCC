from .lock_expr import *

class LocalExpression(InterpretedExpression):
    def __init__(self, var, value, body):
        self.var = var
        self.value = value
        self.body = body

    def eval(self, env: Enviroment):
        env1 = Enviroment()
        env1.set_parent(env)
        val, env1 = self.value.eval(env1)
        dict.__setitem__(env1, self.var, val)
        res, _ = self.body.eval(env1)
        return res, env
