from .local_expr import *

class LambdaExpression(InterpretedExpression):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def eval(self, env):
        def lmbd(value):
            lambda_env = Enviroment({self.var: value})
            lambda_env.set_parent(env)
            y, _ = self.body.eval(lambda_env)
            return y
        return (lmbd, env)

class CallExpression(InterpretedExpression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def eval(self, env):
        f, env = self.name.eval(env)
        v, env = self.value.eval(env)
        return (f(v), env)
