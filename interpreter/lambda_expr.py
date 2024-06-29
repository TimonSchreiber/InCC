from .local_expr import *

class LambdaExpression(InterpretedExpression):
    def __init__(self, vars, body):
        self.vars = vars
        self.body = body

    def eval(self, env: Enviroment):
        def fun(*values):
            if len(values) != len(self.vars):
                raise Exception(f'wrong number of arguments: is {len(values)}, but should be {len(self.vars)}')
            env1 = Enviroment()
            env1.set_parent(env)
            env1 |= {self.vars[i]: values[i] for i in range(len(values))}
            res, _ = self.body.eval(env1)
            return res
        return (fun, env)

class CallExpression(InterpretedExpression):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def eval(self, env: Enviroment):
        fun, env = self.name.eval(env)
        vals = [arg.eval(env)[0] for arg in self.args]
        return (fun(*vals), env)
