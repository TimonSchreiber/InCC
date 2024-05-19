from .comparison_expr import *

class VariableExpression(InterpretedExpression):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return (env[self.name], env)

class AssignmentExpression(InterpretedExpression):
    def __init__(self, v, e):
        self.v = v
        self.e = e

    def eval(self, env):
        value, env = self.e.eval(env)
        env[self.v] = value
        return (value, env)
