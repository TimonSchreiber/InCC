from .sequence_expr import *

class LoopExpression(InterpretedExpression):
    def __init__(self, number, body):
        self.number = number
        self.body = body

    def eval(self, env: Enviroment):
        loops, env = self.number.eval(env)
        res = None
        for _ in range(int(loops)):
            res, env = self.body.eval(env)
        return (res, env)
