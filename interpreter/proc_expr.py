from .struct_expr import *

def tmp(lst):
    for e in lst:
        if e is AssignmentExpression:
            var, expr = e
            if env1.__contains__(var):
                res, env1 = expr.eval(env1)
        else:
            res, env1 = e.eval(env1)
    return res

class ProcExpression(InterpretedExpression):
    def __init__(self, vars, locals, body):
        self.vars = vars
        self.locals = locals
        self.body = body

    def eval(self, env: Enviroment):
        def fun(*values):
            if len(values) != len(self.vars):
                raise Exception(f'wrong number of arguments: is {len(values)}, but should be {len(self.vars)}')
            env1 = Enviroment()
            root = env.get_root()
            env1.set_parent(root)
            env1 |= {self.vars[i]: values[i] for i in range(len(values))}
            env1 |= {self.locals[i]: None for i in range(len(self.locals))}

            lst = self.body.seq if self.body is SequenceExpression else [self.body]
            for e in lst:
                if e is AssignmentExpression:
                    var, expr = e
                    if env1.__contains__(var):
                        res, env1 = expr.eval(env1)
                    else:
                        raise Exception(f'Not allowed to create new variables')
                else:
                    res, env1 = e.eval(env1)

            return res
        return (fun, env)
