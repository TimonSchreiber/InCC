from .local_expr import *

token_set |= {
    'ARROW',
    'COMMA',
    'LAMBDA'
}

t_ARROW  = r'->'
t_COMMA  = r','
t_LAMBDA = r'\\'

# Combine Tokens
tokens = list(token_set | reserved_set)
