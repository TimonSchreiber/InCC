import operator  # used in arithmetic_expr
from .enviroment import Enviroment  # used in local- and lambda_expr

env = Enviroment()

class InterpretedExpression:
    def eval(self, env: Enviroment):
        raise Exception('eval unimplemented')

class SelfEvaluatingExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1

    def eval(self, env: Enviroment):
        return (self.e1, env)

def array2list(arr) :
    return None if arr is None or len(arr) == 0 else (arr[0], ListExpression(arr[1:]))

def head(lst):
    return lst[0]

def tail(lst):
    return lst[1]

def cons(l1, l2):
    return (l1, l2)

class ListExpression(InterpretedExpression):
    def __init__(self, arr):
        self.lst = array2list(arr)

    def eval(self, env: Enviroment):
        if self.lst is None:
            return (None, env)
        return ((self.lst[0].eval(env)[0], self.lst[1].eval(env)[0]), env)

# Add list functions to the enviroment
env |= {
    'head': head,
    'tail': tail,
    'cons': cons
}

class ArrayExpression(InterpretedExpression):
    def __init__(self, arr):
        self.arr = arr

    def eval(self, env: Enviroment):
        return ([elem.eval(env)[0] for elem in self.arr], env)

class ArrayAccessExpression(InterpretedExpression):
    def __init__(self, arr, index):
        self.arr = arr
        self.index = index

    def eval(self, env: Enviroment):
        index, env = self.index.eval(env)
        return (env[self.arr][index], env)
