from .while_expr import *

class ITEExpression(InterpretedExpression):
    def __init__(self, condition, ifbody, elsebody):
        self.condition = condition
        self.ifbody = ifbody
        self.elsebody = elsebody

    def eval(self, env: Enviroment):
        cond, env = self.condition.eval(env)
        if cond:
            return self.ifbody.eval(env)
        if self.elsebody:
            return self.elsebody.eval(env)
        return (None, env)
