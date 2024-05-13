from .ite_expr import *

reserved_set |= {
    'LOCK',
    'IN'
}

# Combine Tokens
tokens = list(token_set | reserved_set)
