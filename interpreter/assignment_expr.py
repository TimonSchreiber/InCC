from .comparison_expr import *

class VariableExpression(InterpretedExpression):
    def __init__(self, name):
        self.name = name

    def eval(self, env: Enviroment):
        return (env[self.name], env)

class AssignmentExpression(InterpretedExpression):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def eval(self, env: Enviroment):
        value, env = self.expr.eval(env)
        env[self.var] = value
        return (value, env)
