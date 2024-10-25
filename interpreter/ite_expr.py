from .while_expr import *

class ITEExpression(InterpretedExpression):
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def eval(self, env: Enviroment):
        cond, env = self.condition.eval(env)
        if cond:
            return self.if_body.eval(env)
        if self.else_body:
            return self.else_body.eval(env)
        return (None, env)
