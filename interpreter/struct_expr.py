from .lambda_expr import *

class StructExpression(InterpretedExpression):
    def __init__(self, body):
        self.body = body

    def eval(self, env):
        env1 = Enviroment()
        env2 = Enviroment()
        env1.set_parent(env)
        return env1, env # ??

class StructMemberAccessExpression(InterpretedExpression):
    def __init__(self, s, dots, id):
        self.s = s
        self.dots = len(dots)
        self.id = id

    def eval(self, env):
        s_env = env[self.s]
        while (self.dots > 1):
            if (s_env.get_parent() is None):
                break
            s_env = s_env.get_parent()
            self.dots = self.dots - 1
        member = s_env[self.id]
        return (member, env)  # ??

class StructExtendExpression(InterpretedExpression):
    def __init__(self, s, body):
        self.s = s
        self.body = body

    def eval(self, env):
        pass