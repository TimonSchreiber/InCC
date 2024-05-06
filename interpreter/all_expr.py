import operator

# TODO: split this into files for each lexer-parser pair

binary_operators = {
    # arithmetic
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    # comparison
    '<':  operator.lt,
    '>':  operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '=':  operator.eq,
    '!=': operator.ne,
    # boolean
    'and':  operator.and_,
    'or':   operator.or_,
    'eq':   operator.eq,
    'xor':  operator.xor,
    'neq':  operator.xor,
    'nand': lambda a,b: not (a and b),
    'nor':  lambda a,b: not (a or b),
    'impl': lambda a,b: (not a) | b
}

unary_operators = {
    # arithmetic
    '-': operator.neg,
    # boolean
    'NOT': operator.not_,
}

boolean_values = {
    'TRUE':  True,
    'FALSE': False
}

class InterpretedExpression:
    def eval(self, env):
        raise Exception('eval unimplemented')

class BinaryOperatorExpression(InterpretedExpression):
    def __init__(self, e1, op, e2):
        self.e1 = e1
        self.op = op
        self.e2 = e2

    def eval(self, env):
        x, env1 = self.e1.eval(env)
        y, env2 = self.e2.eval(env1)
        return (binary_operators[self.op](x, y), env2)

class UnaryOperatorExpression(InterpretedExpression):
    def __init__(self, op, e1):
        self.op = op.upper()
        self.e1 = e1

    def eval(self, env):
        x, env1 = self.e1.eval(env)
        return (unary_operators[self.op](x), env1)

class ParenthesisExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1

    def eval(self, env):
        return self.e1.eval(env)

class SelfEvaluatingExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1

    def eval(self, env):
        return (self.e1, env)

class BooleanValueExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1.upper()

    def eval(self, env):
        return (boolean_values[self.e1], env)

class VariableExpression(InterpretedExpression):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return (env[self.name], env)

class AssignmentExpression(InterpretedExpression):
    def __init__(self, v, e):
        self.v = v
        self.e = e

    def eval(self, env):
        value, env1 = self.e.eval(env)
        env1[self.v] = value
        return (value, env1)

class SequenceExpression(InterpretedExpression):
    def __init__(self, seq):
        self.seq = seq

    def eval(self, env):
        for e in self.seq:
            r, env = e.eval(env)
        return (r, env)

class LoopExpression(InterpretedExpression):
    def __init__(self, number, body):
        self.number = number
        self.body = body

    def eval(self, env):
        n, env = self.number.eval(env)
        r = None
        for _ in range(int(n)):
            r, env = self.body.eval(env)
        return (r, env)

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
