from .lock_expr import *
from .enviroment import Enviroment

class LocalExpression(InterpretedExpression):
    def __init__(self, var, value, body):
        self.var = var
        self.value = value
        self.body = body

    def eval(self, env):
        val, env1 = self.value.eval(env)
        env2 = Enviroment({self.var: val})
        env2.set_parent(env1)
        y, env3 = self.body.eval(env2)
        return (y, env1)
# TODO: what is env3? can I discard it? -> y, _ = self.body.eval(env2)
# Can env1 also be named env? env is not needed...

