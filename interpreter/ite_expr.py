from .while_expr import *

class ITEExpression(InterpretedExpression):
    def __init__(self, condition, ifbody, elsebody):
        self.condition = condition
        self.ifbody = ifbody
        self.elsebody = elsebody

    def eval(self, env):
        t, env = self.condition.eval(env)
        if t:
            return self.ifbody.eval(env)
        elif self.elsebody:
            return self.elsebody.eval(env)
        else:
            return (None, env)
