from .lambda_expr import *

# def access_layer(env: Enviroment, n: int):
#     tmp = env
#     for i in range(n):
#         if tmp.get_parent() is None:
#             raise Exception(f'Inheritance hirachy has not enough layers:\n\t-> Upper limit at {i}, trying to access {n}')
#         tmp = tmp.get_parent()
#     return tmp

class DotVariableExpression(InterpretedExpression):
    def __init__(self, dots, name):
        self.dots = dots
        self.name = name

    def eval(self, env):
        return (env.get_item(self.dots, self.name), env)

class StructExpression(InterpretedExpression):
    def __init__(self, body):
        self.body = body

    def eval(self, env):
        env1 = Enviroment()
        env1.set_parent(env)
        for (id, e) in self.body:  # any parent struct access with dot notation is meaningless
            v, env1 = e.eval(env1)
            dict.__setitem__(env1, id, v)  # add value to this level of dict
        return (env1.get_vals(), env)  # return the enviroment WITHOUT parent

class StructExtendExpression(InterpretedExpression):
    def __init__(self, e, body):
        self.e = e
        self.body = body

    def eval(self, env):
        env1 = Enviroment()
        env1.set_parent(self.e.eval(env)[0])
        for (id, e) in self.body:
            val, env1 = e.eval(env1)
            dict.__setitem__(env1, id, val)  # add value to this level of dict
        return (env1, env)  # return the enviroment WITH parent

class StructMemberAccessExpression(InterpretedExpression):
    def __init__(self, s, dots, id):
        self.s = s
        self.dots = dots
        self.id = id

    def eval(self, env):
        env1 = env[self.s]
        m = env1.get_item(self.dots, self.id)
        return (m, env)
