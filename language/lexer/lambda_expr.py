from .local_expr import *

token_set |= {
    'ARROW',
    'COMMA'
}

t_ARROW = r'->'
t_COMMA = r','

# Combine Tokens
tokens = list(token_set | reserved_set)
