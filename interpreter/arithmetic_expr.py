# import operator
# from .enviroment import Enviroment

from .datatypes import *

binary_operators = {
    # arithmetic
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

unary_operators = {
    # arithmetic
    '-': operator.neg
}

class InterpretedExpression:
    def eval(self, env):
        raise Exception('eval unimplemented')

class BinaryOperatorExpression(InterpretedExpression):
    def __init__(self, e1, op, e2):
        self.e1 = e1
        self.op = op
        self.e2 = e2

    def eval(self, env):
        x, env = self.e1.eval(env)
        y, env = self.e2.eval(env)
        return (binary_operators[self.op](x, y), env)

class UnaryOperatorExpression(InterpretedExpression):
    def __init__(self, op, e1):
        self.op = op.upper()
        self.e1 = e1

    def eval(self, env):
        x, env = self.e1.eval(env)
        return (unary_operators[self.op](x), env)

class ParenthesisExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1

    def eval(self, env):
        return self.e1.eval(env)

class SelfEvaluatingExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1

    def eval(self, env):
        return (self.e1, env)
