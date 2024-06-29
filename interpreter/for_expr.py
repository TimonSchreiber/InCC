from .loop_expr import *

class ForExpression(InterpretedExpression):
    def __init__(self, start, condition, change, body):
        self.start = start
        self.condition = condition
        self.change = change
        self.body = body

    def eval(self, env: Enviroment):
        _, env = self.start.eval(env)
        cond, env = self.condition.eval(env)
        res = None
        while cond:
            res, env = self.body.eval(env)
            _, env = self.change.eval(env)
            cond, env = self.condition.eval(env)
        return (res, env)
