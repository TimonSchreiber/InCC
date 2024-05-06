from .arith_expr import *

token_set |= {
    'LESS_THEN',
    'GREATER_THEN',
    'LESS_EQUALS',
    'GREATER_EQUALS',
    'EQUALS',
    'NOT_EQUALS'
}

t_LESS_THEN         = r'<'
t_GREATER_THEN      = r'>'
t_LESS_EQUALS       = r'<='
t_GREATER_EQUALS    = r'>='
t_EQUALS            = r'='
t_NOT_EQUALS        = r'!='


# Combine Tokens
tokens = list(token_set | reserved_set)
