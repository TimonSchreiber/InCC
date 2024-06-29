from .lambda_expr import *

class DotVariableExpression(InterpretedExpression):
    def __init__(self, dots, name):
        self.dots = dots
        self.name = name

    def eval(self, env: Enviroment):
        var = env.get_item(self.dots, self.name)
        return (var, env)

class StructExpression(InterpretedExpression):
    def __init__(self, body):
        self.body = body

    def eval(self, env: Enviroment):
        env1 = Enviroment()
        env1.set_parent(env)  # set env (local scope) as the parent of this struct
        for (id, expr) in self.body:
            val, env1 = expr.eval(env1)
            dict.__setitem__(env1, id, val)  # add value to this level of dict
        env1 = env1.remove_root()  # remove the root from env1
        return (env1, env)

class StructExtendExpression(InterpretedExpression):
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body

    def eval(self, env: Enviroment):
        struct, _ = self.expr.eval(env)
        env1 = Enviroment()
        env1.set_parent(struct)  # set the parent of this struct
        env1.add_root(env)  # add env (local scope) as the root of this struct
        for (id, expr) in self.body:
            val, env1 = expr.eval(env1)
            dict.__setitem__(env1, id, val)  # add value to this level of dict
        env1 = env1.remove_root()  # remove the root from env1
        return (env1, env)

class StructMemberAccessExpression(InterpretedExpression):
    def __init__(self, expr, dots, id):
        self.expr = expr
        self.dots = dots
        self.id = id

    def eval(self, env: Enviroment):
        struct, _ = self.expr.eval(env)
        val = struct.get_item(self.dots, self.id)
        return (val, env)
