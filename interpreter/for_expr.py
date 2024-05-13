from .loop_expr import *

class ForExpression(InterpretedExpression):
    def __init__(self, start, condition, change, body):
        self.start = start
        self.condition = condition
        self.change = change
        self.body = body

    def eval(self, env):
        _, env = self.start.eval(env)
        t, env = self.condition.eval(env)
        r = None
        while t:
            r, env = self.body.eval(env)
            _, env = self.change.eval(env)
            t, env = self.condition.eval(env)
        return (r, env)
