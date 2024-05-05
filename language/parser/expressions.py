import operator

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


## LOOP
"""
## expr : Loop expression COLON expression ##
def LoopExpression():
    # __init__ (number, body)

    eval
    n, env = self.number.eval(env)
    for _ in range(n):
        r, env = self.body.eval(env)
        return (r, env) """




'''
Loop / For
---
loop expr do expr
for assign; bool_expr; assign do expr
[for assign; bool_expr; assign do lock var expr]  <--  optional
'''
# Was ist der Rückgabewert der Loop-Expression?
# Das Ergebnis der letzen Expression im Körper?
#   -> Was, wenn der Körper gar nicht ausgeführt wurde? 'None'?!


'''
If Then Else
---

IF bool_expr THEN expr
IF bool_expr THEN expr ELSE expr
'''

# precedence 'ELSE' > 'THEN'