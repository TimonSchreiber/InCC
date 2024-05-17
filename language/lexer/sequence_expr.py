from .boolean_expr import *

token_set |= {
    'BEGIN',
    'END',
    'SEPARATOR'
}

t_BEGIN     = r'{'
t_END       = r'}'
t_SEPARATOR = r';'

# Combine Tokens
tokens = list(token_set | reserved_set)
