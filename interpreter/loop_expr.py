from .seque_expr import *

class LoopExpression(InterpretedExpression):
    def __init__(self, number, body):
        self.number = number
        self.body = body

    def eval(self, env):
        n, env = self.number.eval(env)
        r = None
        for _ in range(int(n)):
            r, env = self.body.eval(env)
        return (r, env)
