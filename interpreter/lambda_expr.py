from .local_expr import *

class LambdaExpression(InterpretedExpression):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def eval(self, def_env):
        def lmbd(value):
            new_env = Enviroment({self.var: value})
            new_env.set_parent(def_env)
            y, _ = self.body.eval(new_env)
            return y
        return (lmbd, def_env)

class CallExpression(InterpretedExpression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def eval(self, env):
        f, env = self.name.eval(env)
        v, env = self.value.eval(env)
        return (f(v), env)
    # TODO: call this function f?
