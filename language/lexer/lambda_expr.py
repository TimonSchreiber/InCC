from .local_expr import *

token_set |= {
    'ARROW'
}

t_ARROW = r'->'

# Combine Tokens
tokens = list(token_set | reserved_set)
