import operator  # used in arithmetic_expr
from .enviroment import Enviroment  # used in local- and lambda_expr

class InterpretedExpression:
    def eval(self, env):
        raise Exception('eval unimplemented')

class SelfEvaluatingExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1

    def eval(self, env):
        return (self.e1, env)

def array2list(a) :
    return None if a is None or len(a) == 0 else (a[0], ListExpression(a[1:]))

def head(l):
    return l[0]

def tail(l):
    return l[1]

# def cons(l1, l2):
#     return (l1, l2)

class ListExpression(InterpretedExpression):
    def __init__(self, vals):
        self.vals = array2list(vals)

    def eval(self, env):
        if self.vals is None:
            return None, env
        return ((self.vals[0].eval(env)[0], self.vals[1].eval(env)[0]), env)

class ArrayExpression(InterpretedExpression):
    def __init__(self, vals):
        self.vals = vals

    def eval(self, env):
        return ([self.vals[i].eval(env)[0] for i in range(len(self.vals))], env)

class ArrayAccessExpression(InterpretedExpression):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def eval(self, env):
        i, env = self.index.eval(env)
        return (env[self.name][i], env)
