from .arithmetic_expr import *

binary_operators |= {
    '<':  'le',
    '>':  'gr',
    '<=': 'leq',
    '>=': 'geq',
    '=':  'eq',
    '!=': 'neq'
}
