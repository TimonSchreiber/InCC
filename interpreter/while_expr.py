from .for_expr import *

class WhileExpression(InterpretedExpression):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        t, env = self.condition.eval(env)
        r = None
        while t:
            r, env = self.body.eval(env)
            t, env = self.condition.eval(env)
        return (r, env)
