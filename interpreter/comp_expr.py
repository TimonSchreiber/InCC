from .arith_expr import *

binary_operators.update({
    '<':  operator.lt,
    '>':  operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '=':  operator.eq,
    '!=': operator.ne
})
