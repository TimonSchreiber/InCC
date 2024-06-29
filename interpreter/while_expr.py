from .for_expr import *

class WhileExpression(InterpretedExpression):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env: Enviroment):
        cond, env = self.condition.eval(env)
        res = None
        while cond:
            res, env = self.body.eval(env)
            cond, env = self.condition.eval(env)
        return (res, env)
