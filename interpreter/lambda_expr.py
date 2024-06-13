from .local_expr import *

class LambdaExpression(InterpretedExpression):
    def __init__(self, vars, body):
        self.vars = vars
        self.body = body

    def eval(self, env):
        def lmbd(*values):
            if len(values) != len(self.vars):
                raise Exception(f'wrong number of arguments: is {len(values)}, but should be {len(self.vars)}')
            lmbd_env = Enviroment()
            lmbd_env.set_parent(env)
            lmbd_env |= {self.vars[i]: values[i] for i in range(len(values))}
            y, _ = self.body.eval(lmbd_env)
            return y
        return (lmbd, env)

class CallExpression(InterpretedExpression):
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def eval(self, env):
        f, env = self.name.eval(env)
        v = [val.eval(env)[0] for val in self.values]
        return (f(*v), env)
