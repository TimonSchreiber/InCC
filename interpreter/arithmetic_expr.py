import operator
from .enviroment import Enviroment

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
        x, env1 = self.e1.eval(env)
        y, env2 = self.e2.eval(env1)
        return (binary_operators[self.op](x, y), env2)

class UnaryOperatorExpression(InterpretedExpression):
    def __init__(self, op, e1):
        self.op = op.upper()
        self.e1 = e1

    def eval(self, env):
        x, env1 = self.e1.eval(env)
        return (unary_operators[self.op](x), env1)

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
