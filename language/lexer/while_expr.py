from .for_expr import *

reserved_set |= {
    'WHILE'
}

# Combine Tokens
tokens = list(token_set | reserved_set)
